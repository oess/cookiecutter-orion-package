from cuberecord import (OEMolRecordCube,
                        InputMoleculeFieldParameter,
                        MolRecordInputPort,
                        InitMolRecordMixin)
from openeye.oechem import OECalculateMolecularWeight


class MWFilterCube(OEMolRecordCube):
    title = "Molecular Weight Filter"
    description = "Sends record with a molecule to the success port of the molecule has a lower" \
                  "molecular weight than the molecule sent to the init port (else no outputted)."
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight"]

    init = MolRecordInputPort("init", initializer=True)
    init_mol_field = InputMoleculeFieldParameter("init_mol_field", title="Initializer Mol Field")

    in_mol_field = InputMoleculeFieldParameter("in_mol_field")

    def begin(self):
        self._mw_cutoff = None
        for record in self.init:
            if record.has_value(self.args.init_mol_field):
                mol = record.get_value(self.args.init_mol_field)
                self._mw_cutoff = OECalculateMolecularWeight(mol)
                break

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mol = record.get_value(self.args.in_mol_field)
            mw = OECalculateMolecularWeight(mol)
            if mw < self._mw_cutoff:
                self.success.emit(record)


class MixinExampleMWFilterCube(OEMolRecordCube, InitMolRecordMixin):
    title = "Molecular Weight Filter"
    description = "Sends record with a molecule to the success port of the molecule has a lower" \
                  "molecular weight than the molecule sent to the init port (else no outputted)."
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight"]

    in_mol_field = InputMoleculeFieldParameter("in_mol_field")

    def begin(self):
        self._mw_cutoff = None
        for mol in self.get_init_molecules():
            self._mw_cutoff = OECalculateMolecularWeight(mol)
            break

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mol = record.get_value(self.args.in_mol_field)
            mw = OECalculateMolecularWeight(mol)
            if mw < self._mw_cutoff:
                self.success.emit(record)
