import unittest
import BitArrayX_test

def my_module_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(BitArrayX_test)
    return suite