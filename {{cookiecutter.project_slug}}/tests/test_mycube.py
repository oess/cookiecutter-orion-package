from unittest import TestCase
from {{cookiecutter.module_name}} import MyCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord


class BooleanSwitchTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MyCube("Boolean Switch")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_true(self):
        # set_parameters must be called before calling start
        self.test_runner.set_parameters(switch=True)

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

    def test_false(self):
        record = OERecord()
        self.test_runner.set_parameters(switch=False)
        self.test_runner.start()
        self.test_runner.cube.process(record, "intake")
        self.test_runner.finalize()
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 0)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 1)