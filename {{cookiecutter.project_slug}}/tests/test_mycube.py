from unittest import TestCase
from {{cookiecutter.module_name}} import MyCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord


class MyCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MyCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        num_to_send = 10
        for i in range(num_to_send):
            record = OERecord()
            self.test_runner.cube.process(record, "intake")

        # This calls the end process on the cube
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), num_to_send)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)
