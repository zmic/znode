
import unittest
import json
import numpy as np
from znode import json_loads

class znode_test1(unittest.TestCase):

    def reproduce(self, n): 
        x = n.eval()
        y = json_loads(n.json_dumps()).eval()
        if isinstance(x, np.ndarray):
            return self.assertTrue((x==y).all())
        return self.assertEqual(x, y)

    def test1(self):    
        from znode import ŋstandard_normal, ŋrg_MT19937, ŋintegers, ŋint, ŋtuple, json_loads
    
        n = ŋstandard_normal(ŋrg_MT19937(ŋint(12)),(3,4))
        x = n.eval()
        self.assertAlmostEqual(x[0][0], -0.48977262 )
        x = n.dump()
        self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [(3, 4)]], ['ŋstandard_normal', [1, 2]]])
        x = json.dumps(n.dump())
        self.assertEqual(x, r'[["\u014bint", [12]], ["\u014brg_MT19937", [0]], ["\u014btuple", [[3, 4]]], ["\u014bstandard_normal", [1, 2]]]')
        x = json.loads(json.dumps(n.dump()))
        self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [[3, 4]]], ['ŋstandard_normal', [1, 2]]])
        n2 = json_loads(n.json_dumps())
        x = n2.eval()
        self.assertAlmostEqual(x[0][0], -0.48977262 )

        self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))))
        self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), (3, 4))))

        n = ŋrg_MT19937(12)
        n = ŋintegers(n, 0, 10, (4,4))
        self.reproduce(n)

    def test2(self):
        from znode import ŋnp_indices, ŋndtype

        n = ŋnp_indices((3,4))
        x = n.eval()
        self.assertEqual(x[0][1][1],1)
        self.assertEqual(x.shape, (2,3,4))
        self.reproduce(n)

        n1 = ŋndtype(np.float32)
        self.assertEqual(str(n1),"ŋndtype(ŋstr('float32'))")
        self.reproduce(n1)
        n2 = ŋndtype("float32")
        self.assertEqual(str(n2),"ŋndtype(ŋstr('float32'))")
        self.reproduce(n2)

        x = n1.eval()
        n = ŋnp_indices((3,4), np.float32)
        x = n.eval()
        self.assertEqual(x[1][1][3],3)
        self.assertEqual(x.dtype,np.float32)
        self.assertEqual(n.json_dumps(), r'[["\u014btuple", [[3, 4]]], ["\u014bstr", ["float32"]], ["\u014bndtype", [1]], ["\u014bnp_indices", [0, 2]]]')
        self.reproduce(n)

if __name__ == '__main__':
    unittest.main()
    

