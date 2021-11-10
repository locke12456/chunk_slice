import unittest, utils

class Test_utils_test(unittest.TestCase):
    def test_01_Compress(self):
        test = utils.CompressFiles("compress", "compress")
        self.assertEqual(1,1)
    def test_02_Slice(self):
        test = utils.SliceFile(1024*1024, "compress.tar.gz", "compress.json")
        self.assertEqual(1,1)
    def test_03_Verify(self):
        test = utils.VerifyChunks("compress.tar.gz_out")
        self.assertEqual(1,1)
if __name__ == '__main__':
    unittest.main()
