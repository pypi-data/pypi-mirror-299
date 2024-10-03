import unittest
from autogenerator.generator import generate_modules
import os

class TestAutoModuleGenerator(unittest.TestCase):
    def setUp(self):
        self.script = """
import os
import sys

def foo():
    print("foo")

def bar():
    print("bar")
"""
        self.imports = ['import os']
        self.functions = ['foo']
        self.output_dir = 'test_generated'

    def test_generate_modules(self):
        generate_modules(self.script, self.imports, self.functions, self.output_dir)
        expected_file = os.path.join(self.output_dir, 'foo.py')
        self.assertTrue(os.path.exists(expected_file))
        with open(expected_file, 'r') as f:
            content = f.read()
            self.assertIn('import os', content)
            self.assertIn('def foo():', content)

    def tearDown(self):
        # Clean up generated files
        import shutil
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

if __name__ == '__main__':
    unittest.main()
