import unittest
from chemhelp.help import mol_to_smiles


class TestHelp(unittest.TestCase):
    def test_mol_to_smiles(self):
        from rdkit import Chem

        mol = Chem.MolFromSmiles("CC")
        self.assertEqual(mol_to_smiles(mol), "CC")
