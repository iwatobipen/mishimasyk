from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
import json, sys

class Node(object):
    def __init__(self,mol):
        self.mol = mol
    def mw( self ):
        return round( Descriptors.MolWt( self.mol ), 2 )
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


def make_nodes( mols , degrees):
    nodes = []
    for i, mol in enumerate( mols[:300] ):
        molid = i
        node = Node( mol )
        smi = node.smi()
        mw = node.mw()
        data = { "data" : { "id":"mol_"+str(molid), "molid":molid, "smi": smi, "molwt": mw, "degree": degrees["mol_"+str(i)] }}
        nodes.append( data )
    return nodes

def make_edges( mols, cutoff=0.80 ):
    edges = []
    degrees = {}
    for i in range( len( mols[:300] )):
        for j in range( i ):
            edge = Edge(mols[i], mols[j])
            degrees.setdefault("mol_"+str(i),1)
            degrees.setdefault("mol_"+str(j),1)
            if edge.sim() >= cutoff and edge.sim() < 1.0:
                #print edge.sim()
                degrees[ "mol_"+str(i) ] += 1
                degrees[ "mol_"+str(j) ] += 1
                data = { "data": { "id":str(i)+">>"+str(j),"similarity": edge.sim() ,"source": "mol_"+str(i), "target": "mol_"+str(j) }}
                edges.append( data )
    return edges, degrees

    
if __name__=="__main__":
    mols = [mol for mol in Chem.SDMolSupplier(sys.argv[1]) ]
    edges, degrees = make_edges( mols, cutoff = 0.75 )
    nodes = make_nodes( mols , degrees )
    data = { "nodes":nodes, "edges":edges}
    f = open("../static/jsondata/mols.json","w")
    f.write(json.dumps(data, indent=4))
    f.close()
