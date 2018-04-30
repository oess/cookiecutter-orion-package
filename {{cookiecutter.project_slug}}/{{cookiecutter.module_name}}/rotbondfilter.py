from cuberecord import (OEMolRecordCube, InMolFieldMixin)
from openeye.oechem import OEIsRotor, OECount
from floe.api import IntegerParameter


class RotatableBondFilterCube(OEMolRecordCube, InMolFieldMixin):
    title = "Rotatable Bond Filter"
    description = "Filters records that have more than a given number of rotatable bonds by " \
                  "sending the those records to the failure port.  All others to success port."
    classification = [["Filter", "Rotatable Bonds"]]
    tags = ["Example", "Filter", "Rotatable Bonds"]

    max_rotors = IntegerParameter("max_rotors",
                                  title="Max Rotors",
                                  required=True,
                                  description="maximum number of rotors")

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mol = record.get_value(self.args.in_mol_field)
            rot_count = 0
            for bond in mol.GetBonds(OEIsRotor()):
                rot_count += 1
            if rot_count > self.args.max_rotors:
                self.failure.emit(record)
            else:
                self.success.emit(record)
        else:
            self.failure.emit(record)
