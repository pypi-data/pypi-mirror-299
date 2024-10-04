from rdkit import Chem


def mol_to_smiles(mol):
    return Chem.MolToSmiles(mol)
