from unittest import TestCase
from {{cookiecutter.module_name}} import MyRocsCube
from cuberecord import OERecordCubeTestRunner, OEMolRecordStream
from datarecord import OERecord, OEPrimaryMolField
from openeye.oechem import OEMol, OESmilesToMol
from os import path


def _smi_to_record(smi):
    record = OERecord()
    mol = OEMol()
    OESmilesToMol(mol, smi)
    record.set_value(OEPrimaryMolField(), mol)
    return record


class MyCubeTest(TestCase):
    TEST_DIR = path.join(path.dirname(__file__), 'test_data')
    TEST_FILE = path.join(TEST_DIR, 'drugs.sdf')

    @classmethod
    def _create_cube(cls):
        return MyRocsCube("Test Cube")

    def setUp(self):
        self.test_runner = OERecordCubeTestRunner(self._create_cube())

    def test_cube(self):
        # Send query to initialization port
        init_records = []
        for record in OEMolRecordStream(path.join(self.TEST_DIR, "benzene.sdf")):
            init_records.append(record)
        self.test_runner.set_init_port_records("init", init_records)

        # This calls the begin function of the cube
        self.test_runner.start()

        # We pass records to the process function this way
        for record in OEMolRecordStream(path.join(self.TEST_DIR, "hexane.oeb.gz")):
            self.test_runner.cube.process(record, "intake")

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
        self.assertEqual(mol.NumConfs(), 1)
