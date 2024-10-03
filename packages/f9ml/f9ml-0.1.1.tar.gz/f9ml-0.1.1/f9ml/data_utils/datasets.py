import logging

import h5py
import numpy as np
import torch
from torch.utils.data import Dataset, IterableDataset


class NpDataset(Dataset):
    def __init__(self, processors, split_idx, save_scalers=False, get_labels=False):
        """General dataset class for numpy data. The data is processed by the processors graph and split into train,
        validation and test sets. The data is then returned as a torch.Tensor. All data is loaded into memory.

        Parameters
        ----------
        processors: dict of DataProcessor
            Data processors.
        split_idx : np.array
            Indices of the data split (train, test or val).
        save_scalers : bool, optional
            Save scalers in dataset object.
        stage : str or None, optional
            Training stage, by default None.
        get_labels : bool, optional
            Use labels, if False return X, if True return X and y labels, by default False.
        """
        super().__init__()
        self.save_scalers, self.scalers = save_scalers, {}
        self.get_labels = get_labels

        output_processor = processors["output"]
        data, self.selection, scalers = output_processor.data, output_processor.selection, output_processor.scalers

        data = data[split_idx]

        if self.save_scalers:
            self.scalers = scalers

        if get_labels:
            features = self.selection[self.selection["type"] != "label"]
            labels = self.selection[self.selection["type"] == "label"]

            self.X = torch.from_numpy(data[:, features.index]).to(torch.float32)
            self.y = torch.from_numpy(data[:, labels.index]).to(torch.float32)
        else:
            self.X = torch.from_numpy(data).to(torch.float32)
            self.y = None

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        if self.y is not None:
            return self.X[idx], self.y[idx]
        else:
            return self.X[idx]


class HDF5DataGenerator:
    def __init__(
        self,
        processors_graph,
        file_path,
        hdf5_loader,
        shape,
        chunks_idx,
        split_idx,
        worker_id=0,
        save_scalers=False,
        get_labels=False,
        return_graph=False,
    ):
        self.processors_graph = processors_graph
        self.file_path = file_path
        self.hdf5_loader = hdf5_loader

        self.dataset_name = self.hdf5_loader.dataset_name
        self.chunk_size = self.hdf5_loader.chunk_size

        self.shape = shape
        self.chunks_idx = chunks_idx
        self.split_idx = split_idx
        self.worker_id = worker_id

        self.save_scalers, self.scalers = save_scalers, {}
        self.selection = None

        self.return_graph = return_graph

        self.get_labels = get_labels
        self.features_idx, self.labels_idx = None, None

        self.n_chunks = self.shape[0] // self.chunk_size + 1
        self.current_item = 0
        self.current_chunk_idx = 0
        self.current_shape = self.chunks_idx[self.current_chunk_idx].shape

    def run_processors_graph(self, chunk_data):
        self.hdf5_loader.chunk_data = chunk_data
        fitted_processors = self.processors_graph.fit()

        outputs = fitted_processors["output"]

        if self.save_scalers:
            if self.current_chunk_idx not in self.scalers:
                self.scalers[self.current_chunk_idx] = outputs.scalers

        if self.selection is None:
            self.selection = outputs.selection

        return fitted_processors

    def setup_labels(self):
        features = self.selection[self.selection["type"] != "label"]
        labels = self.selection[self.selection["type"] == "label"]

        features_idx, labels_idx = features.index, labels.index

        return features_idx, labels_idx

    def load_chunk(self):
        """Load the next chunk of data that fits into memory from disk.

        Returns
        -------
        torch.Tensor
            Chunk of data.
        """
        if self.current_chunk_idx == self.n_chunks:
            raise StopIteration

        logging.debug(f"Loading chunk {self.current_chunk_idx}/{len(self.chunks_idx) - 1} on worker {self.worker_id}!")

        chunk_idx = self.chunks_idx[self.current_chunk_idx]

        # this ensures that data is randomly split into train, val and test given by split_idx
        chunk_data = np.empty((len(chunk_idx), self.shape[1]), dtype=np.float32)
        with h5py.File(self.file_path, "r") as f:
            for i in range(len((chunk_idx))):
                random_i = self.split_idx[self.current_chunk_idx][i]
                chunk_data[i, :] = f[self.dataset_name][random_i]

        fitted_processors = self.run_processors_graph(chunk_data)
        chunk_data = fitted_processors["output"].data

        self.current_chunk_idx += 1

        self.chunk_data = torch.from_numpy(chunk_data).to(torch.float32)
        self.current_shape = self.chunk_data.shape

        if self.get_labels:
            self.features_idx, self.labels_idx = self.setup_labels()

        return self.chunk_data

    def get_len(self):
        return len(self.split_idx)

    def get_item(self):
        if self.current_item % self.current_shape[0] == 0:
            self.load_chunk()
            self.current_item = 0

        if self.get_labels:
            item = (
                self.chunk_data[self.current_item, self.features_idx],
                self.chunk_data[self.current_item, self.labels_idx],
            )
        else:
            item = self.chunk_data[self.current_item]

        self.current_item += 1

        if self.return_graph:
            return item, self.processors_graph
        else:
            return item

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_item()


class HDF5Dataset(IterableDataset):
    def __init__(
        self,
        processors_graph,
        split_idx,
        save_scalers,
        get_labels=False,
        return_graph=False,
    ):
        """Create an iterable dataset from an hdf5 file. The data is split into chunks of size `chunk_size` and then
        split into train, validation and test sets. The data is then processed by the processors graph and returned.
        Data is loaded lazily, so only the current chunk is loaded into memory.

        Parameters
        ----------
        processors_graph : DataProcessorsGraph
            Data processors graph.
        split_idx : np.array
            Indices of the data split (train, test or val).
        save_scalers : bool, optional
            Save scalers as dict with current chunk index as key, by default False.
        get_labels : bool, optional
            Use labels, if False return X, if True return X and y labels, by default False.
        return_graph : bool, optional
            If True will return (X, fitted graph) or ((X, y), fitted graph), by default False.
        """
        super().__init__()
        self.processors_graph = processors_graph
        self.split_idx = split_idx
        self.save_scalers = save_scalers
        self.get_labels = get_labels

        self.return_graph = return_graph

        self.processors_graph.copy_processors = True  # need to run each processor multiple times

        self.file_path = self.processors_graph.processors["input"].file_path

        self.hdf5_loader = self.processors_graph.processors["hdf5_loader"]
        self.dataset_name = self.hdf5_loader.dataset_name
        self.chunk_size = self.hdf5_loader.chunk_size

        self.shape = (self.split_idx.shape[0], self.hdf5_loader.get_shape()[1])
        self.chunks_idx = self.setup_chunks()
        self.splits = self.setup_splits()

    def get_shape(self):
        with h5py.File(self.file_path, "r") as f:
            return f[self.dataset_name].shape

    def setup_chunks(self):
        """Split the data in hdf5 into chunks of size `chunk_size`.

        Returns
        -------
        list of arrays
            Indices of the data chunks.
        """
        n_chunks = self.shape[0] // self.chunk_size + 1

        idx = np.arange(0, self.shape[0], 1)
        chunks_idx = np.array_split(idx, n_chunks)

        self.current_shape = chunks_idx[0].shape

        return chunks_idx

    def setup_splits(self):
        splits = []
        for chunk_idx in self.chunks_idx:
            chunk_split = self.split_idx[chunk_idx]
            splits.append(chunk_split)
        return np.array_split(self.split_idx, len(self.chunks_idx))

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is not None:
            worker_id = worker_info.id
        else:
            worker_id = 0

        num_workers = worker_info.num_workers if worker_info is not None else 1
        self.hdf5_loader.num_workers = num_workers

        worker_split_chunks_idx = []
        worker_split_splits = []
        worker_shape_splits = []

        if len(self.chunks_idx) < num_workers:
            raise ValueError(f"Number of chunks ({len(self.chunks_idx)}) must be < num_workers ({num_workers})!")

        for i in range(num_workers):
            worker_split_chunks_idx.append(self.chunks_idx[i::num_workers])
            worker_split_splits.append(self.splits[i::num_workers])
            worker_shape_splits.append((sum([s.shape[0] for s in worker_split_chunks_idx[-1]]), self.shape[1]))

        return HDF5DataGenerator(
            self.processors_graph,
            self.file_path,
            self.hdf5_loader,
            shape=worker_shape_splits[worker_id],
            chunks_idx=worker_split_chunks_idx[worker_id],
            split_idx=worker_split_splits[worker_id],
            worker_id=worker_id,
            save_scalers=self.save_scalers,
            get_labels=self.get_labels,
            return_graph=self.return_graph,
        )
