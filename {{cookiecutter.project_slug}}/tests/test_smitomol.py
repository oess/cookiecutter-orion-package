from unittest import TestCase
from training_package import SmiToMolCube
from cuberecord import OERecordCubeTestRunner
from datarecord import OERecord, OEField, Types


class SmiToMolCubeTest(TestCase):
    @classmethod
    def _create_cube(cls):
        return SmiToMolCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_success(self):
        # Create a record to pass to the cube
        smi_field_name = "Smi"
        record = OERecord()
        record.set_value(OEField(smi_field_name, Types.String), "CC")

        # Choose a name for the output molecule field
        mol_field_name = "Mol"

        # Set the parameters (before calling start)
        self.test_runner.set_parameters(smi_field=smi_field_name, out_mol_field=mol_field_name)

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        self.test_runner.cube.process(record, "intake")

        # This calls the end process on the cube
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)
        self.assertEqual(self.test_runner.outputs["missing"].qsize(), 0)

        # Check that we have a molecule on the record that came out of the success port
        record = self.test_runner.outputs["success"].get()
        self.assertTrue(record.has_value(OEField(mol_field_name, Types.Chem.Mol)))

    def test_failure(self):
        # Create a record to pass to the cube
        smi_field_name = "Smi"
        record = OERecord()
        record.set_value(OEField(smi_field_name, Types.String), "foobar198")

        # Choose a name for the output molecule field
        mol_field_name = "Mol"

        # Set the parameters (before calling start)
        self.test_runner.set_parameters(smi_field=smi_field_name, out_mol_field=mol_field_name)

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        self.test_runner.cube.process(record, "intake")

        # This calls the end process on the cube
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 0)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 1)
        self.assertEqual(self.test_runner.outputs["missing"].qsize(), 0)

        # Make sure we don't have a molecule since we failed
        record = self.test_runner.outputs["failure"].get()
        self.assertFalse(record.has_value(OEField(mol_field_name, Types.Chem.Mol)))

    def test_missing(self):
        # Create a record to pass to the cube
        smi_field_name = "Smi"
        record = OERecord()

        # Choose a name for the output molecule field
        mol_field_name = "Mol"

        # Set the parameters (before calling start)
        self.test_runner.set_parameters(smi_field=smi_field_name, out_mol_field=mol_field_name)

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        self.test_runner.cube.process(record, "intake")

        # This calls the end process on the cube
        self.test_runner.finalize()

        # Now check the output
        self.assertEqual(self.test_runner.outputs["success"].qsize(), 0)
        self.assertEqual(self.test_runner.outputs["failure"].qsize(), 0)
        self.assertEqual(self.test_runner.outputs["missing"].qsize(), 1)

        # Make sure we don't have a molecule since we failed
        record = self.test_runner.outputs["missing"].get()
        self.assertFalse(record.has_value(OEField(mol_field_name, Types.Chem.Mol)))