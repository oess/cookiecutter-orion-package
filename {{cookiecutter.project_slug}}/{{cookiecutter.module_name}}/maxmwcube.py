from cuberecord import (OEMolRecordCube, InputMoleculeFieldParameter, InMolFieldMixin)
from openeye.oechem import OECalculateMolecularWeight


class MaxMWCube(OEMolRecordCube):
    title = "Max Molecular Weight"
    description = "Outputs the record with the largest molecule, by MW.  Discards the rest"
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight", "Max", "Filter"]

    in_mol_field = InputMoleculeFieldParameter("in_mol_field")

    def __init__(self, name, **kwargs):
        super(MaxMWCube, self).__init__(name, **kwargs)
        self._max_mw = None
        self._max_record = None

    def begin(self):
        self._max_mw = 0.0
        self._max_record = None

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mw = OECalculateMolecularWeight(record.get_value(self.args.in_mol_field))
            if mw > self._max_mw:
                self._max_mw = mw
                self._max_record = record

    def end(self):
        if self._max_record is not None:
            self.success.emit(self._max_record)


# Same functionality as the cube above, but uses the InMolFieldMixin
# instead of declaring in_mol_field explicitly
class MixinExampleMaxMWCube(OEMolRecordCube, InMolFieldMixin):
    title = "Max Molecular Weight"
    description = "Outputs the record with the largest molecule, by MW.  Discards the rest"
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight", "Max", "Filter"]

    def begin(self):
        self._max_mw = 0.0
        self._max_record = None

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mw = OECalculateMolecularWeight(record.get_value(self.args.in_mol_field))
            if mw > self._max_mw:
                self._max_mw = mw
                self._max_record = record

    def end(self):
        if self._max_record is not None:
            self.success.emit(self._max_record)
