from rdkit import Chem
from rdkit.Chem import rdDepictor, AllChem
from rdkit.Chem.Draw import rdMolDraw2D



def depictmol( smiles, core ):
    #mol = Chem.MolFromSmiles( smiles  )
    mol = Chem.MolFromSmiles( smiles  )
    atoms = mol.GetSubstructMatch(Chem.MolFromSmarts( core ))
    try:
        Chem.Kekulize( mol )
        rdDepictor.Compute2DCoords( mol )
    except:
        rdDepictor.Compute2DCoords( mol )
    drawer = rdMolDraw2D.MolDraw2DSVG( 300, 200 )
    
    drawer.DrawMolecule( mol, highlightAtoms=atoms )
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText().replace( 'svg:', '' )
    return svg