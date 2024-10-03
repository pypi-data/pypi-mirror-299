import os
import sys
import unittest

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from nfetoolkit import nfetk

class TestNFeRep(unittest.TestCase):
           
    def test_rep(self):
        
        nfeToolkit = nfetk.NFeRepository()
        nfeToolkit.store_all('.', verbose=True)
        nfeToolkit.save('nfe_data.txt')
        self.assertIsNotNone(nfeToolkit.content)
        
if __name__ == '__main__':
    unittest.main()