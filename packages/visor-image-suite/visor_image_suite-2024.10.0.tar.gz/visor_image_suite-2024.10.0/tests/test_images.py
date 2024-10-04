import os
import unittest

from visor_image.images import (
    VisorRawImage,
)

class TestImages(unittest.TestCase):

    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), 'data', 'TEST001')
        self.visor_raw_image = VisorRawImage(self.sample_path)

    def test_visor_raw_image_struct(self):
        image_struct = self.visor_raw_image.image_struct
        # expected_struct = {
        #     'struct': {
        #         'Slice_1.zarr': {
        #             '561nm_10X': {
        #                 'Stack_1': ['Resolution_Level_1']
        #             }
        #         }
        #     },
        #     'channels': ['560nm_10X'],
        #     'slices': ['Slice_1'],
        # }
        self.assertIn('struct', image_struct)
        self.assertEqual(image_struct['struct']['Slice_1']['561nm_10X']['Stack_1'], ['Resolution_Level_1'])
        self.assertEqual(image_struct['channels'], ['561nm_10X'])
        self.assertEqual(image_struct['slices'], ['Slice_1'])

if __name__ == '__main__':
    unittest.main()