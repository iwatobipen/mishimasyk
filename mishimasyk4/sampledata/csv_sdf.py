from rdkit import Chem
import pandas as pd
import sys
df = pd.read_csv(sys.argv[1],header=0)
writer = Chem.SDWriter(sys.argv[1].split(".")[0]+".sdf")

for smi in df["SMILES"]:
    writer.write(Chem.MolFromSmiles(smi))

writer.close()


