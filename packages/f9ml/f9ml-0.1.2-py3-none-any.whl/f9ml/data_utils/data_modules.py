import logging
import multiprocessing

import lightning as L
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from f9ml.data_utils.datasets import HDF5Dataset, NpDataset


def get_splits(n_data, train_split, val_split):
    """Utility function for splitting data using [`sklearn.model_selection.train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).

    Parameters
    ----------
    n_data : int
        Number of data points.
    train_split : float
        Percentage (in range 0.0 to 1.0) of data for training.
    val_split : float or None
        Percentage (in range 0.0 to 1.0) of data for validation.

    Note
    ----
    If `val_split=None`, no test data is returned. If `train_split=1.0`, returns only shuffled training data.

    Returns
    -------
    tuple
        Tuple with random indices for training, validation and test data.
    """
    idx = np.arange(n_data)

    if train_split == 1.0:
        np.random.shuffle(idx)
        return idx, [], []

    remaining, train_idx = train_test_split(idx, test_size=train_split)

    if val_split is None:
        return train_idx, remaining, []
    else:
        test_idx, val_idx = train_test_split(idx[remaining], test_size=val_split)

    logging.debug(f"Created splits with sizes: {len(train_idx)}, {len(val_idx)}, {len(test_idx)}")
    return train_idx, val_idx, test_idx


class BaseDataModule(L.LightningDataModule):
    def __init__(
        self,
        processors_graph,
        train_split=0.7,
        val_split=None,
        save_scalers=False,
        get_labels=False,
        **dataloader_kwargs,
    ):
        """Base class for data modules.

        Parameters
        ----------
        processors_graph : DataProcessorsGraph
            Processors graph with fit() method. Should have output processor as a node at the end.
        train_split : float, optional
            Train split, by default 0.7.
        val_split : float, optional
            Validation split, by default 0.5. If None is passed, no test split is done.
        save_scalers : bool, optional
            Save scalers for data preprocessors.
        get_labels : bool, optional
            Get labels (X and y) from the DataLoader.
        dataloader_kwargs : dict, optional
            Kwargs for torch.utils.data.DataLoader. If `num_workers=-1` will use all available workers.

        Other parameters
        ----------------
        selection : pd.DataFrame
            Selection of data.
        scalers : dict
            Scalers for data preprocessors.
        train_idx : np.ndarray
            Random indices for training data.
        val_idx : np.ndarray
            Random indices for validation data.
        test_idx : np.ndarray
            Random indices for test data.
        train : torch.utils.data.Dataset
            Torch training dataset.
        val : torch.utils.data.Dataset
            Torch validation dataset.
        test : torch.utils.data.Dataset
            Torch test dataset.
        _is_split : bool
            Flag for checking if data is already split to test/val/test.

        """
        super().__init__()

        self.processors_graph = processors_graph
        self.train_split, self.val_split = train_split, val_split
        self.save_scalers = save_scalers
        self.get_labels = get_labels
        self.dataloader_kwargs = dataloader_kwargs

        self.selection, self.scalers = None, None

        self.train_idx, self.val_idx, self.test_idx = None, None, None
        self.train, self.val, self.test = None, None, None
        self._is_split = False

        if self.dataloader_kwargs.get("num_workers") == -1:
            self.dataloader_kwargs["num_workers"] = multiprocessing.cpu_count()

    def prepare_data(self):
        return None

    def teardown(self, stage=None):
        if stage == "fit" or stage is None:
            self.train, self.val = None, None

        if stage == "test":
            self.test = None

        self.stage = stage

    def train_dataloader(self):
        return DataLoader(self.train, shuffle=True, **self.dataloader_kwargs)

    def val_dataloader(self):
        return DataLoader(self.val, shuffle=False, **self.dataloader_kwargs)

    def test_dataloader(self):
        return DataLoader(self.test, shuffle=False, **self.dataloader_kwargs)


class MemoryDataModule(BaseDataModule):
    def __init__(self, *args, **kwargs):
        """Memory data module for in-memory data."""
        super().__init__(*args, **kwargs)

    def setup(self, stage=None):
        """Setup method for data module.

        Parameters
        ----------
        stage : str or None, optional
            Stage of the setup by lightning.
        """
        processors = self.processors_graph.fit()

        self.selection = processors["output"].selection
        self.scalers = processors["output"].scalers

        if not self._is_split:
            self.train_idx, self.val_idx, self.test_idx = get_splits(
                len(processors["output"].data), self.train_split, self.val_split
            )
        else:
            self._is_split = True

        if stage == "fit" or stage is None:
            self.train = NpDataset(
                processors,
                self.train_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )
            self.val = NpDataset(
                processors,
                self.val_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )

        if stage == "test":
            self.test = NpDataset(
                processors,
                self.test_idx,
                save_scalers=self.save_scalers,
                get_labels=self.get_labels,
            )


class DiskDataModule(BaseDataModule):
    def __init__(
        self,
        *args,
        return_graph=False,
        train_num_workers,
        val_num_workers=None,
        test_num_workers=None,
        **kwargs,
    ):
        """Disk data module for data stored on disk."""
        super().__init__(*args, **kwargs)
        self.return_graph = return_graph

        if val_num_workers is None:
            val_num_workers = train_num_workers
        if test_num_workers is None:
            test_num_workers = train_num_workers

        self.num_workers = [train_num_workers, val_num_workers, test_num_workers]
        self.num_workers = [multiprocessing.cpu_count() if i == -1 else i for i in self.num_workers]
        self.dataloader_kwargs.pop("num_workers", None)

    def setup(self, stage=None):
        """Setup method for data module.

        Parameters
        ----------
        stage : str or None, optional
            Stage of the setup by lightning.
        """
        self.processors_graph.processors["hdf5_loader"].file_path = self.processors_graph.processors["input"].file_path

        if not self._is_split:
            self.train_idx, self.val_idx, self.test_idx = get_splits(
                self.processors_graph.processors["hdf5_loader"].get_shape()[0], self.train_split, self.val_split
            )
        else:
            self._is_split = True

        if stage == "fit" or stage is None:
            self.train = HDF5Dataset(
                self.processors_graph,
                self.train_idx,
                self.save_scalers,
                get_labels=self.get_labels,
                return_graph=self.return_graph,
            )
            self.val = HDF5Dataset(
                self.processors_graph,
                self.val_idx,
                self.save_scalers,
                get_labels=self.get_labels,
                return_graph=self.return_graph,
            )

        if stage == "test":
            self.test = HDF5Dataset(
                self.processors_graph,
                self.test_idx,
                self.save_scalers,
                get_labels=self.get_labels,
                return_graph=self.return_graph,
            )

    def train_dataloader(self):
        return DataLoader(self.train, num_workers=self.num_workers[0], **self.dataloader_kwargs)

    def val_dataloader(self):
        return DataLoader(self.val, num_workers=self.num_workers[1], **self.dataloader_kwargs)

    def test_dataloader(self):
        return DataLoader(self.test, num_workers=self.num_workers[2], **self.dataloader_kwargs)
