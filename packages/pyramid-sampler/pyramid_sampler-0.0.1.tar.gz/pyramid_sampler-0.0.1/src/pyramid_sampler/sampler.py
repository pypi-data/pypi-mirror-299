from __future__ import annotations

import numba
import numpy as np
import numpy.typing as npt
import zarr
from dask import array as da
from dask import compute, delayed

from ._logging import sampler_log


@numba.jit  # type: ignore[misc]
def _coarsen(
    output_shape: tuple[int, int, int],
    level_coarse: int,
    level_fine: int,
    refine_factor: tuple[int, int, int],
    covered_vals: npt.NDArray,
) -> npt.NDArray[np.float64]:
    d_level = level_coarse - level_fine

    lev0_npixels_0 = refine_factor[0] ** d_level
    lev0_npixels_1 = refine_factor[1] ** d_level
    lev0_npixels_2 = refine_factor[2] ** d_level

    output_array = np.zeros(output_shape, dtype=np.float64)

    for i0_coarse in range(output_shape[0]):
        i0_fine_0 = i0_coarse * refine_factor[0] ** d_level
        i0_fine_1 = i0_fine_0 + lev0_npixels_0

        for i1_coarse in range(output_shape[1]):
            i1_fine_0 = i1_coarse * refine_factor[1] ** d_level
            i1_fine_1 = i1_fine_0 + lev0_npixels_1
            for i2_coarse in range(output_shape[2]):
                i2_fine_0 = i2_coarse * refine_factor[2] ** d_level
                i2_fine_1 = i2_fine_0 + lev0_npixels_2
                val = 0.0
                nvals = 0.0
                for i0 in range(i0_fine_0, i0_fine_1):
                    for i1 in range(i1_fine_0, i1_fine_1):
                        for i2 in range(i2_fine_0, i2_fine_1):
                            val += covered_vals[i0, i1, i2]
                            nvals += 1.0
                val = float(val / nvals)
                output_array[i0_coarse, i1_coarse, i2_coarse] = val

    return output_array


class Downsampler:
    """
    A class for downsampling a pre-existing 3D zarr array.
    """

    def __init__(
        self,
        zarr_store_path: str,
        refine_factor: npt.ArrayLike,
        level_0_res: npt.ArrayLike,
        chunks: npt.ArrayLike | None = None,
    ):
        self.refine_factor = np.asarray(refine_factor).astype(int)
        self.finest_resolution = np.asarray(level_0_res).astype(int)
        assert len(self.refine_factor) == len(self.finest_resolution)
        self.zarr_store_path = zarr_store_path
        self.ndim = len(self.refine_factor)
        if chunks is None:
            chunks = (64,) * self.ndim
        self.chunks = np.asarray(chunks).astype(int)

    def _get_fine_ijk(
        self,
        ijk_coarse: npt.ArrayLike,
        level_coarse: int,
        level_fine: int,
    ) -> npt.NDArray[np.int64]:
        ijk_coarse = np.asarray(ijk_coarse).astype(int)
        d_level = level_coarse - level_fine
        ijk_0 = ijk_coarse * self.refine_factor**d_level
        return ijk_0.astype(int)

    def _get_level_shape(
        self,
        level_coarse: int,
    ) -> npt.NDArray[np.int64]:
        d_level = level_coarse - 0
        return self.finest_resolution // self.refine_factor**d_level

    def _get_global_start_index(
        self, chunk_linear_index: int, level: int
    ) -> tuple[npt.NDArray[np.int64], npt.NDArray[np.int64]]:
        lev_shape = self._get_level_shape(level)
        chunksizes_by_dim = self._get_chunks_by_dim(lev_shape)
        n_chunks_by_dim = [len(ch) for ch in chunksizes_by_dim]
        chunk_index = np.unravel_index(chunk_linear_index, n_chunks_by_dim)
        ndims = self.ndim
        si = []
        ei = []
        for idim in range(ndims):
            dim_chunks = np.array(chunksizes_by_dim[idim], dtype=int)

            covered_chunks = dim_chunks[0 : chunk_index[idim]]
            si.append(np.sum(covered_chunks).astype(int))
            ei.append(si[-1] + chunksizes_by_dim[idim][chunk_index[idim]])

        si = np.array(si, dtype=int)
        ei = np.array(ei, dtype=int)
        return si, ei

    def _get_level_nchunks(self, level_shape: npt.ArrayLike) -> npt.NDArray[np.int64]:
        level_shape = np.asarray(level_shape).astype(int)
        return np.array(level_shape) // np.array(self.chunks)

    def _get_chunks_by_dim(self, level_shape: npt.ArrayLike) -> npt.NDArray[np.int64]:
        chunks = self.chunks
        nchunks = self._get_level_nchunks(level_shape)
        chunksizes = []
        for dim in range(len(chunks)):
            dim_chunks = []
            for _ in range(nchunks[dim]):
                dim_chunks.append(chunks[dim])
            chunksizes.append(dim_chunks)
        return np.array(chunksizes, dtype=int)

    def _downsample_by_one_level(
        self,
        coarse_level: int,
        zarr_field: str,
    ) -> None:
        level = coarse_level
        fine_level = level - 1
        lev_shape = self._get_level_shape(level)
        field1 = zarr.open(self.zarr_store_path)[zarr_field]
        field1.empty(level, shape=lev_shape, chunks=self.chunks)

        numchunks = field1[str(level)].nchunks

        chunk_writes = []
        for ichunk in range(numchunks):
            chunk_writes.append(
                delayed(_write_chunk_values)(
                    self, ichunk, level, fine_level, zarr_field
                )
            )

        _ = compute(*chunk_writes)

    def downsample(
        self,
        max_levels: int,
        zarr_field: str,
    ) -> None:
        if max_levels <= 0:
            msg = f"max_level must exceed 0, found {max_levels}"
            raise ValueError(msg)

        for level in range(1, max_levels):
            lev_shape = self._get_level_shape(level)
            nchunks_by_dim = self._get_level_nchunks(lev_shape)
            if np.any(nchunks_by_dim == 0):
                msg = f"cannot subdivide further, stopping downsampling at level {level-1}."
                sampler_log.info(msg)
                break
            msg = f"downsampling to level {level}."
            sampler_log.info(msg)
            self._downsample_by_one_level(level, zarr_field)


def _write_chunk_values(
    downsampler: Downsampler, ichunk: int, level: int, fine_level: int, zarr_field: str
) -> int:
    refine_factor = downsampler.refine_factor
    zarr_file = downsampler.zarr_store_path

    si, ei = downsampler._get_global_start_index(ichunk, level)
    chunksize = ei - si

    # read in the index range of the fine level covered by this chunk
    si0 = downsampler._get_fine_ijk(si, level, fine_level)
    ei0 = downsampler._get_fine_ijk(ei, level, fine_level)

    # actually read in the covered values. this assumes we can hold
    # at least prod(refine_factor) * chunksize in memory, e.g.,
    # for refinement factor of (2,2,2) and chunksize of (64,64,64), the
    # covered array will have size of 8 * 64**3 = 2_097_152
    fine_zarr = zarr.open(zarr_file)[zarr_field][str(fine_level)]
    covered_vals = fine_zarr[si0[0] : ei0[0], si0[1] : ei0[1], si0[2] : ei0[2]]

    outvals = _coarsen(
        tuple(chunksize),
        level,
        fine_level,
        tuple(refine_factor),
        covered_vals,
    )

    coarse_zarr = zarr.open(zarr_file)[zarr_field][str(level)]
    coarse_zarr[si[0] : ei[0], si[1] : ei[1] :, si[2] : ei[2]] = outvals

    return 1


def initialize_test_image(
    zarr_store: zarr.storage.Store,
    zarr_field: str,
    base_resolution: tuple[int, int, int],
    chunks: int | tuple[int, int, int] | None = None,
    overwrite_field: bool = True,
) -> None:
    field1 = zarr_store.create_group(zarr_field, overwrite=overwrite_field)

    if chunks is None:
        chunks = (64, 64, 64)
    lev0 = da.random.random(base_resolution, chunks=chunks)
    halfway = np.asarray(base_resolution) // 2
    lev0[0 : halfway[0], 0 : halfway[1], 0 : halfway[2]] = (
        lev0[0 : halfway[0], 0 : halfway[1], 0 : halfway[2]] + 0.5
    )
    field1.empty(0, shape=base_resolution, chunks=chunks)
    da.to_zarr(lev0, field1["0"])
