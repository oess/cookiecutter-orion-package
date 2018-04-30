from cuberecord import OEProcessMolCube
from openeye.oeomega import OEOmega


class MyOmegaCube(OEProcessMolCube):
    def begin(self):
        self._omega = OEOmega()

    def process_mol(self, mol):
        self._omega(mol)
        return mol
