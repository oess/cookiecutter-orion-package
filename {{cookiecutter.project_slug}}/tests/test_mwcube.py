from unittest import TestCase
from trai{{cookiecutter.module_name}}ning_package import MWCube, MWPropCube, ParallelMWPropCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OESmilesToMol, OECalculateMolecularWeight, OEMol


class MWCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MWCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        mol = OEMol()
        OESmilesToMol(mol, "CCC")
        record = OERecord()
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")

        # This tells the test runner the cube is done getting records
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)

        mol_field = self.test_runner.cube.args.in_mol_field
        mw_field = self.test_runner.cube.args.mw_field

        record = self.test_runner.outputs["success"].get()

        self.assertTrue(record.has_value(mol_field))
        self.assertTrue(record.has_value(mw_field))
        mw = OECalculateMolecularWeight(record.get_value(mol_field))
        self.assertAlmostEqual(mw, record.get_value(mw_field), places=2)


class MWPropCubeTest(MWCubeTest):
    @classmethod
    def _create_cube(cls):
        return MWPropCube("Test Cube")


class ParallelMWPropCubeTest(MWCubeTest):
    @classmethod
    def _create_cube(cls):
        return ParallelMWPropCube("Test Cube")
