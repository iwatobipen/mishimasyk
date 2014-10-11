from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs

class Node(object):
    def __init__(self,mol):
        self.mol = mol
    def mw( mol ):
        return Descriptors.MolWt( mol )
    def smi( mol ):
        return Chem.MolToSmiles( mol )

class Edge(object):
    def __init__(self, mol1, mol2 ):
        self.mol1 = mol1
        self.mol2 = mol2
    def source( self ):
        return Chem.MolToSmiles( self.mol1 )
    def target( self ):
        return Chem.MolToSmiles( self.mol2 )
    def sim(self):
        fp1 = AllChem.GetMorganFingerprintAsBitVect(self.mol1, 2)
        fp2 = AllChem.GetMorganFingerprintAsBitVect(self.mol2, 2)
        tc = DataStructs.TanimotoSimilarity(fp1,fp2)
        return tc



        



