
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

    def test0(self):    
        from znode import ŋintegers, ŋint, ŋtuple, ŋnp_array
    
        n = ŋtuple(1,2,3)
        self.assertEqual(n.eval(), (1,2,3))
        self.reproduce(n)
        n = ŋtuple(1,2,(3,(),(3,)))
        self.assertEqual(n.eval(), (1, 2, (3, (), (3,))))
        self.reproduce(n)

        a = ŋint(1)
        b = ŋint(2)
        n = ŋtuple(a+b,a-b)
        self.assertEqual(n.eval(), (3,-1))

        a = ŋnp_array(((1,2),(3,4)), np.float32)
        self.reproduce(a)

    def test1(self):    
        from znode import ŋstandard_normal, ŋrg_MT19937, ŋintegers, ŋint, ŋtuple, json_loads
    
        n = ŋstandard_normal(ŋrg_MT19937(ŋint(12)),(3,4))
        x = n.eval()
        self.assertAlmostEqual(x[0][0], -0.48977262 )
        x = n.dump()
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [(3, 4)]], ['ŋstandard_normal', [1, 2]]])
        x = json.dumps(n.dump())
        #self.assertEqual(x, r'[["\u014bint", [12]], ["\u014brg_MT19937", [0]], ["\u014btuple", [[3, 4]]], ["\u014bstandard_normal", [1, 2]]]')
        x = json.loads(json.dumps(n.dump()))
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [[3, 4]]], ['ŋstandard_normal', [1, 2]]])
        n2 = json_loads(n.json_dumps())
        x = n2.eval()
        self.assertAlmostEqual(x[0][0], -0.48977262 )

        #self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))))
        #self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), (3, 4))))

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
        self.reproduce(n)

    def test3(self):
        from znode import ŋnp_indices, ŋnp_transpose, ŋrandom, ŋnp_RandomState, ŋnp_concatenate, ŋtuple, ŋnp_reshape
        x = 8
        n = ŋnp_transpose(ŋnp_indices((x,x)), (1,2,0))
        self.reproduce(n)
        n = n + 0.5
        self.reproduce(n)
        n2 = n*(1/x)
        self.reproduce(n2)
        n1 = (1/x)*n
        self.reproduce(n1)

        n1 = ŋnp_reshape(n1, (x*x,2))
        self.reproduce(n1)

        nr = ŋnp_RandomState(32)
        n2 = ŋrandom(nr, (x*x,1))
        n2 = n2 / 10
        self.reproduce(n2)
        n1 = ŋnp_concatenate((n1, n2), 1)
        self.reproduce(n1)

if __name__ == '__main__':
    unittest.main()
    

