from unittest import TestCase
from {{cookiecutter.module_name}} import MaxMWCube, MixinExampleMaxMWCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OESmilesToMol, OECalculateMolecularWeight, OEMol


class MaxMWCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MaxMWCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        mol = OEMol()
        record = OERecord()

        OESmilesToMol(mol, "CCC")
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")
        OESmilesToMol(mol, "CCCC")
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")
        OESmilesToMol(mol, "CCCCC")
        record.set_value(OEPrimaryMolField(), mol)
        self.test_runner.cube.process(record, "intake")

        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)

        mol_field = self.test_runner.cube.args.in_mol_field

        record = self.test_runner.outputs["success"].get()

        self.assertTrue(record.has_value(mol_field))
        mw_cube = OECalculateMolecularWeight(record.get_value(mol_field))
        mw_biggest = OECalculateMolecularWeight(mol)
        self.assertAlmostEqual(mw_cube, mw_biggest, places=2)


class MixinExampleMaxMWCubeTest(MaxMWCubeTest):
    @classmethod
    def _create_cube(cls):
        return MixinExampleMaxMWCube("TestCube")
