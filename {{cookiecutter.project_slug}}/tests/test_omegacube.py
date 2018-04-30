from unittest import TestCase
from {{cookiecutter.module_name}} import MyOmegaCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OEMol, OESmilesToMol


def _smi_to_record(smi):
    record = OERecord()
    mol = OEMol()
    OESmilesToMol(mol, smi)
    record.set_value(OEPrimaryMolField(), mol)
    return record


class MyCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return MyOmegaCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        self.test_runner.cube.process(_smi_to_record("CCCCCC"), "intake")

        # This calls the end process on the cube
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)

        # Get the output record
        record = self.test_runner.outputs["success"].get()
        mol_field = self.test_runner.cube.args.out_mol_field
        self.assertTrue(record.has_value(mol_field))
        mol = record.get_value(mol_field)
        self.assertGreaterEqual(mol.NumConfs(), 2)
