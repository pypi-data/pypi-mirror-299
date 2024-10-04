import os

class VisorRawImage:

    # sample_path: os.path.join(data_dir, sample_id)
    def __init__(self, sample_path):

        raw_image_path = os.path.join(sample_path, 'VISoR_Raw_Images')

        if not os.path.isdir(raw_image_path):
            raise NotADirectoryError(f'The path {raw_image_path} is not a directory')

        self.path = sample_path
        self.image_struct = self._get_image_struct(raw_image_path)

    # Ref: https://github.com/visor-tech/visor-data-schema/blob/main/image-data-schema.md
    # image_struct:
    # slice dict
    #   channel dict per slice
    #       stack dict per channel
    #           resolution list per stack
    def _get_image_struct(self, raw_image_path):
        image_struct = {
            "struct": {},       # the structure of this raw image
            "channels": [],     # channel list
            "slices": [],       # slice list
        }
        slice_dirs = [f for f in os.listdir(raw_image_path)
                      if os.path.isdir(os.path.join(raw_image_path, f))
                      and f.startswith('Slice_')
                      ]
        if len(slice_dirs) == 0:
            raise FileNotFoundError(f'The path {raw_image_path} does not contain zarr files start with "Slice_".')

        image_struct['slices'] = [slice_dir.replace('.zarr','') for slice_dir in slice_dirs]

        for slice_dir in slice_dirs:
            image_struct['struct'][slice_dir.replace('.zarr','')] = {}
            slice_path = os.path.join(raw_image_path, slice_dir)
            channel_dirs = [f for f in os.listdir(slice_path)
                            if os.path.isdir(os.path.join(slice_path, f))
                            ]

            image_struct['channels'] = list(set(image_struct['channels']+channel_dirs))

            for channel_dir in channel_dirs:
                image_struct['struct'][slice_dir.replace('.zarr','')][channel_dir] = {}
                channel_path = os.path.join(slice_path, channel_dir)
                stack_dirs = [f for f in os.listdir(channel_path)
                              if os.path.isdir(os.path.join(channel_path, f))
                              and f.startswith('Stack_')
                              ]
                for stack_dir in stack_dirs:
                    stack_path = os.path.join(channel_path, stack_dir)
                    resolution_dirs = [f for f in os.listdir(stack_path)
                                    if os.path.isdir(os.path.join(stack_path, f))
                                    ]
                    image_struct['struct'][slice_dir.replace('.zarr','')][channel_dir][stack_dir] = resolution_dirs
        return image_struct
