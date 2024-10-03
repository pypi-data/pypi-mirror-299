from __future__ import annotations

from typing import TYPE_CHECKING, List

import numpy as np
from napari.layers import Points

from ._slice import _PointSliceRequest, _ThickNDSlice

if TYPE_CHECKING:
    from napari.layers.utils._slice_input import _SliceInput

__all__ = [
    "BroadcastablePoints",
]


class BroadcastablePoints(Points):
    def __init__(
        self, data=None, *, ndim=None, broadcast_dims: List[int] = None, **kwargs
    ):
        """
        Parameters
        ----------
        data :
        """
        if broadcast_dims is None:
            broadcast_dims = []
        # sort to ensure the for loop works correctly
        self._broadcast_dims = sorted(broadcast_dims)
        if data is not None:
            for b in broadcast_dims:
                # need to loop so because doing all at once means that larger
                # values for dim will be placed in the wrong spot
                # data = np.insert(data, b, -np.ones(data.shape[0]), axis=1)
                data = np.insert(data, b, 0, axis=1)

        super().__init__(data, ndim=ndim, **kwargs)

    def last_displayed(self) -> np.ndarray:
        """
        Return the XY coordinates of the most recently displayed points

        Returns
        -------
        data : (N, 2)
            The xy coordinates of the most recently displayed points.
        """
        return self._view_data

    def _make_slice_request_internal(
        self, slice_input: _SliceInput, data_slice: _ThickNDSlice
    ) -> _PointSliceRequest:
        self._lastResponse = _PointSliceRequest(
            broadcast_dims=self._broadcast_dims,
            slice_input=slice_input,
            data=self.data,
            data_slice=data_slice,
            projection_mode=self.projection_mode,
            out_of_slice_display=self.out_of_slice_display,
            size=self.size,
        )
        return self._lastResponse
