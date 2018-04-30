from cuberecord import (OEMolRecordCube,
                        OEMolPropertyCube,
                        InputMoleculeFieldParameter,
                        FloatFieldParameter)
from openeye.oechem import OECalculateMolecularWeight
from floe.api import ParallelMixin


class MWCube(OEMolRecordCube):
    title = "Molecular Weight"
    description = "Compute Molecular Weight Cube"
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight"]

    in_mol_field = InputMoleculeFieldParameter("in_mol_field")
    mw_field = FloatFieldParameter("mw_field", default="MW Field")

    def process(self, record, port):
        if record.has_value(self.args.in_mol_field):
            mol = record.get_value(self.args.in_mol_field)
            mw = OECalculateMolecularWeight(mol)
            record.set_value(self.args.mw_field, mw)
            self.success.emit(record)
        else:
            self.failure.emit(record)


# This cube is functionally identical to the one above, but uses
# inherits from OEMolPropertyCube instead of OEMolRecordCube
class MWPropCube(OEMolPropertyCube):
    title = "Molecular Weight"
    description = "Compute Molecular Weight Cube"
    classification = [["Properties", "Molecular Weight"]]
    tags = ["Example", "Property", "Molecular Weight"]

    mw_field = FloatFieldParameter("mw_field", default="MW Field")

    def get_property(self, mol):
        return OECalculateMolecularWeight(mol)


# For ParallelMixins it is is important that the mixin come first
class ParallelMWPropCube(ParallelMixin, MWPropCube):
    title = "Parallel " + MWPropCube.title
