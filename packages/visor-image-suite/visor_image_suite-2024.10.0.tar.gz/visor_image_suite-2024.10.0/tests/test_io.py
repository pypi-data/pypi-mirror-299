import os
import unittest
import shutil

from visor_image.io import (
    write_raw_stack,
    read_raw_stack,
)

class TestIO(unittest.TestCase):

    def setUp(self):

        # initiate VisorRawImage reader
        self.sample_path = os.path.join(os.path.dirname(__file__), 'data', 'TEST001')
        self.channel = '561nm_10X'
        self.resolution_level = 1
        self.slice_index = 1
        self.stack_index = 1

    def tearDown(self):
        tmp_dir = os.path.join(self.sample_path, 'tmp')
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)


    def test_read_raw_stack(self):
        raw_stack = read_raw_stack(self.sample_path,
                                   self.slice_index,
                                   self.channel,
                                   self.stack_index,
                                   self.resolution_level)
        self.assertEqual(raw_stack.shape, (4,4,4))

    def test_write_raw_stack(self):
        fake_array = read_raw_stack(self.sample_path,
                                    self.slice_index,
                                    self.channel,
                                    self.stack_index,
                                    self.resolution_level)
        write_raw_stack(fake_array,
                        os.path.join(self.sample_path,'tmp'),
                        self.slice_index,
                        self.channel,
                        self.stack_index,
                        self.resolution_level)

        raw_stack_dir = os.path.join(self.sample_path,'tmp',
                                     'VISoR_Raw_Images',
                                     'Slice_1.zarr',
                                     '561nm_10X',
                                     'Stack_1',
                                     'Resolution_Level_1')
        self.assertTrue(os.path.exists(raw_stack_dir))

        raw_stack_array = read_raw_stack(os.path.join(self.sample_path,'tmp'),
                                         self.slice_index,
                                         self.channel,
                                         self.stack_index,
                                         self.resolution_level)
        self.assertEqual(raw_stack_array.shape, (4,4,4))

if __name__ == '__main__':
    unittest.main()