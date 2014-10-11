from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
import json, sys

class Node(object):
    def __init__(self,mol):
        self.mol = mol
    def mw( self ):
        return Descriptors.MolWt( self.mol )
    def smi( self ):
        return Chem.MolToSmiles( self.mol )

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


def make_nodes( mols ):
    nodes = []
    for i, mol in enumerate( mols[:300] ):
        molid = i
        node = Node( mol )
        smi = node.smi()
        mw = node.mw()
        data = { "data" : { "molid":molid, "smi": smi }}
        nodes.append( data )
    return nodes

def make_edges( mols, cutoff=0.80 ):
    edges = []
    for i in range( len( mols[:300] )):
        for j in range( i ):
            edge = Edge(mols[i], mols[j])
            if edge.sim() >= cutoff:
                #print edge.sim()
                data = { "data": { "id":str(i)+">>"+str(j),"similarity": edge.sim() ,"source": edge.source(), "target": edge.target() }}
                edges.append( data)
    return edges


    
if __name__=="__main__":
    mols = [mol for mol in Chem.SDMolSupplier(sys.argv[1]) ]
    nodes = make_nodes( mols )
    edges = make_edges( mols ,cutoff=0.85)
    data = { "nodes":nodes, "edges":edges}
    f = open("mols.json","w")
    f.write(json.dumps(data, indent=4))
    f.close()
