from cuberecord import (OEMolRecordCube,
                        OutputMoleculeFieldParameter,
                        StringFieldParameter,
                        RecordOutputPort)
from openeye.oechem import OESmilesToMol, OEMol


class SmiToMolCube(OEMolRecordCube):
    title = "Smiles to Mol"
    description = "Converts a string field with smiles into an OEMol and attaches it to the record"
    classification = [["Converters", "Smiles"]]
    tags = ["Example", "Converters", "Smiles", "OEMol"]

    missing = RecordOutputPort("missing")

    smi_field = StringFieldParameter("mw_field", default="MW Field")
    out_mol_field = OutputMoleculeFieldParameter("in_mol_field")

    def process(self, record, port):
        if record.has_value(self.args.smi_field):
            smi = record.get_value(self.args.smi_field)
            mol = OEMol()
            if OESmilesToMol(mol, smi):
                record.set_value(self.args.out_mol_field, mol)
                self.success.emit(record)
            else:
                self.failure.emit(record)
        else:
            self.missing.emit(record)
