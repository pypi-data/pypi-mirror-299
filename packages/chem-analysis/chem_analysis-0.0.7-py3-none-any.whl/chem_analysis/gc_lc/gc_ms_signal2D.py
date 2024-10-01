import logging
import pathlib
from typing import Sequence

import numpy as np

from chem_analysis.base_obj.unify_methods_2d import UnifyMethod2D, UnifyMethodMS2D
from chem_analysis.base_obj.signal_2d import Signal2D
from chem_analysis.mass_spec.ms_signal_3D import MSSignal3D
from chem_analysis.gc_lc.gc_ms_signal import GCMSSignal

logger = logging.getLogger(__name__)


class GCMSSignal2D(Signal2D):
    _signal = GCMSSignal

    def __init__(self,
                 ms: MSSignal3D,
                 x_label: str = None,
                 y_label: str = None,
                 z_label: str = None,
                 name: str = None
                 ):
        x_label = x_label or "retention time"
        y_label = y_label or "time"
        z_label = z_label or "intensity"
        z_raw = np.sum(ms.w_raw, axis=2)
        super().__init__(ms.y_raw, ms.z_raw, z_raw, x_label, y_label, z_label, name)
        self.ms = ms

    def recompute_from_ms(self):
        self.x_raw = self.ms.y_raw
        self.y_raw = self.ms.z_raw
        self.z_raw = np.sum(self.ms.w_raw, axis=2)
        self.processor.processed = False

    def get_signal(self, y_index: int, processed: bool = True, copy_: bool = False) -> GCMSSignal:
        """

        Parameters
        ----------
        y_index
        processed:
            True: get x, z
            False: get x_raw, z_raw
        copy_:
            True: data will be a copy.
            False: data will be a view (until edited)

        Returns
        -------

        Should return a 'view' and not 'copy'. But will become a copy if edited.
        https://numpy.org/doc/stable/user/basics.copies.html

        """
        if processed:
            x, y, ms = self.x, self.z[y_index, :], self.ms.get_signal(y_index, processed=processed)
        else:
            x, y, ms = self.x_raw, self.z_raw[y_index, :], self.ms.get_signal(y_index, processed=processed)

        if copy_:
            x, y, ms = None, None, self.ms.get_signal(y_index, copy_=True)

        sig = self._signal(x=x, y=y, ms=ms, x_label=self.x_label, y_label=self.y_label,
                           name=f"slice_{self.y_label}: {self.y[y_index]}", id_=y_index)
        sig.extract_value = self.y[y_index]
        if not processed:
            sig.processor = self.processor.get_copy()
        return sig

    @classmethod
    def from_signals(cls,
                     signals: Sequence[GCMSSignal],
                     y: np.ndarray = None,
                     y_label: str = None,
                     unify_method: UnifyMethod2D = UnifyMethodMS2D(),
                     ):  # -> Signal2D
        if y is None:
            y = np.arange(len(signals))
        else:
            if len(y.shape) != 1 and y.shape[0] == len(signals):
                raise ValueError("The number of signals must be the same as the number of y points.\n"
                                 f"\tnumber of signals: {len(signals)}\n\tnumber of y points:{y.shape[0]}")

        x_label = signals[0].x_label
        z_label = signals[0].y_label
        ms = MSSignal3D.from_signals([sig.ms_raw for sig in signals], y, y_label, unify_method)
        return cls(ms=ms, x_label=x_label, y_label=y_label, z_label=z_label)

    def to_npz(self, path: str | pathlib.Path, sparse: bool = True, **kwargs):
        """Save an array to a binary file in NumPy ``.npz`` format."""
        self.ms.to_npz(path, sparse=sparse, **kwargs)

    @classmethod
    def from_npz(cls, path: str | pathlib.Path):
        ms = MSSignal3D.from_npz(path)
        return cls(ms)
