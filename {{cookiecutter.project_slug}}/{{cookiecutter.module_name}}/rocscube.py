from cuberecord import OEProcessMolCube, InitMolRecordMixin
from openeye.oeshape import OEOverlapPrep, OEOverlapFunc, OEOverlapResults
from openeye.oechem import OEMol


class MyRocsCube(OEProcessMolCube, InitMolRecordMixin):
    def begin(self):
        query = None
        for mol in self.get_init_molecules():
            query = mol
            break

        # Setup the prep
        self._prep = OEOverlapPrep()
        self._prep.Prep(query)
        self._overlap = OEOverlapFunc()
        self._overlap.SetupRef(query)

    def process_mol(self, mol):
        out_mol = None
        best_score = None
        for conf in mol.GetConfs():
            res = OEOverlapResults()
            self._prep.Prep(conf)
            if self._overlap.Overlap(conf, res):
                if best_score is None or res.GetTanimotoCombo() > best_score:
                    out_mol = OEMol(conf)
                    best_score = res.GetTanimotoCombo()
        return out_mol
