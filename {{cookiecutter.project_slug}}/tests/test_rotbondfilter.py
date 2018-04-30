from unittest import TestCase
from {{cookiecutter.module_name}} import RotatableBondFilterCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OESmilesToMol, OEMol


def _smi_to_record(smi):
    record = OERecord()
    mol = OEMol()
    OESmilesToMol(mol, smi)
    record.set_value(OEPrimaryMolField(), mol)
    return record


class MWFilterCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return RotatableBondFilterCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # Set test parameters
        self.test_runner.set_parameters(max_rotors=4)

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        self.test_runner.cube.process(_smi_to_record("C"), "intake")
        self.test_runner.cube.process(_smi_to_record("CC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCCCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCCCCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCCCCCC"), "intake")
        self.test_runner.cube.process(_smi_to_record("CCCCCCCCC"), "intake")

        # This tells the test runner the cube is done getting records
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 7)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 2)