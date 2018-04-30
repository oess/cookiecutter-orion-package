from unittest import TestCase
from training_package import MWFilterCube, MixinExampleMWFilterCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OESmilesToMol, OEMol


class MWFilterCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MWFilterCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # Make record with molecule for the initializer port
        mol = OEMol()
        OESmilesToMol(mol, "CC")
        record = OERecord()
        record.set_value(OEPrimaryMolField(), mol)

        # Setup the test to send the init record to the initializer port
        self.test_runner.set_init_port_records("init", records=[record])

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        OESmilesToMol(mol, "CCC")
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")
        OESmilesToMol(mol, "C")
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")

        # This tells the test runner the cube is done getting records
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)


class MixinExampleMWFilterTestCube(MWFilterCubeTest):
    @classmethod
    def _create_cube(cls):
        return MixinExampleMWFilterCube("Test Cube")
