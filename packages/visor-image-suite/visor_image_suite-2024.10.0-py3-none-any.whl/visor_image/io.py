import os
import dask.array as da
from numcodecs import Blosc

def read_raw_stack(path:str,
                   slice_index:int, channel:str,
                   stack_index:int, resolution_level:int):
    """
    Read the raw stack.

    Parameters:
    path             : the sample path (data directory plus sample name)
    slice_index      : e.g. 1
    channel          : e.g. 561nm_10X
    stack_index      : e.g. 1
    resolution_level : e.g. 1 ~ raw, 3 ~ 4x downsample

    Returns:
    dask.array: the stack array
    """
    array_path = os.path.join(path,
                              'VISoR_Raw_Images',
                              f'Slice_{str(slice_index)}.zarr',
                              channel,
                              f'Stack_{str(stack_index)}',
                              f'Resolution_Level_{str(resolution_level)}')
    return da.from_zarr(array_path)

def write_raw_stack(array:da.Array, path:str,
                    slice_index:int, channel:str,
                    stack_index:int, resolution_level:int,
                    compression:str='zstd',
                    clevel:int=5):
    """
    Write to the raw stack.

    Parameters:
    path             : the sample path (data directory plus sample name)
    slice_index      : e.g. 1
    channel          : e.g. 561nm_10X
    stack_index      : e.g. 1
    resolution_level : e.g. 1 ~ raw, 3 ~ 4x downsample
    compression      : Blosc compression algorithm, e.g. 'zstd'
    clevel           : Blosc compression level, 0-9
                       0 ~ fast & low compression
                       5 ~ balance
                       9 ~ slow & high compression

    Returns:
    None
    """
    zarr_file = os.path.join(path,
                             'VISoR_Raw_Images',
                             f'Slice_{str(slice_index)}.zarr')
    component = os.path.join(channel,
                             f'Stack_{str(stack_index)}',
                             f'Resolution_Level_{str(resolution_level)}')
    da.to_zarr(array, zarr_file,
               component=component,
               compressor=Blosc(cname=compression, clevel=clevel))
