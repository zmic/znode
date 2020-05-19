
import unittest
import json


class znode_test1(unittest.TestCase):

    def test1(self):
        from znode import ŋstandard_normal, ŋrg_MT19937, ŋint, ŋtuple, json_loads

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

if __name__ == '__main__':
    unittest.main()
    

