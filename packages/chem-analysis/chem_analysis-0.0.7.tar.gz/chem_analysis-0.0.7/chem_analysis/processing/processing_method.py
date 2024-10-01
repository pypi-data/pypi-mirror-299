import abc

import numpy as np

from chem_analysis.utils.code_for_subclassing import MixinSubClassList


class ProcessingMethod(MixinSubClassList, abc.ABC):

    def __init__(self, temporal_processing: int = 1):
        """

        Parameters
        ----------
        temporal_processing:
            0: data is not a time series
            1: data is a time series in 1 dimension
            2: data is a time series in 2 dimension
        """
        self.temporal_processing = temporal_processing

    @abc.abstractmethod
    def run(self, x: np.ndarray, data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        ...

    def run2D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self.temporal_processing >= 1:
            return self._run2D_temporal(x, y, z)
        return self._run2D(x, y, z)

    @abc.abstractmethod
    def _run2D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ...

    def _run2D_temporal(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """ y-axis is taken to be time series """
        for i in range(z.shape[0]):
            _, z[i, :] = self.run(x, z[i, :])
        return x, y, z

    def run3D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) \
            -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        if self.temporal_processing >= 1:
            self.temporal_processing -= 1  # reduce number of dimensions left as timeseries
            x, y, z, w = self._run3D_temporal(x, y, z, w)
            self.temporal_processing += 1  # reset original dimensions that are timeseries
            return x, y, z, w
        return self._run3D(x, y, z, w)

    @abc.abstractmethod
    def _run3D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) \
            -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        ...
    
    def _run3D_temporal(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) \
            -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """ z-axis is taken to be time series """
        for i in range(z.shape[0]):
            _, _, z[i, :] = self.run2D(x, y, z[i, :])
        return x, y, z, w


class Translation(ProcessingMethod, abc.ABC):
    ...


class Smoothing(ProcessingMethod, abc.ABC):
    ...


class Resampling(ProcessingMethod, abc.ABC):
    ...


class PhaseCorrection(ProcessingMethod, abc.ABC):
    ...


class FourierTransform(ProcessingMethod, abc.ABC):
    ...


class Edit(ProcessingMethod, abc.ABC):
    ...


class Baseline(ProcessingMethod, abc.ABC):
    def __init__(self,
                 temporal_processing: int = 1,
                 save_result: bool = False
                 ):
        super().__init__(temporal_processing)

        # for saving intermediate results
        self.save_result = save_result
        self.baseline = None
        self.x = None
        self.data = None

    def run(self, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        baseline = self.get_baseline(x, y)
        data = y - baseline
        data[y==0] = 0

        if self.save_result:
            self.baseline = baseline
            self.x = x
            self.data = y

        return x, data

    @abc.abstractmethod
    def get_baseline(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        ...

    def _run2D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        raise NotImplementedError()

    def _run3D(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, w: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        raise NotImplementedError()
