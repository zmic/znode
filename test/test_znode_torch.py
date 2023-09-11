import unittest
import json
import numpy as np
import znode
import ast
import torch


def json_dumps(n):
    #return json.dumps(n.dump())
    return repr(n.dump())

def json_loads(s):
    #return znode.load(json.loads(s))
    return znode.load(ast.literal_eval(s))

class znode_test1(unittest.TestCase):

    def reproduce(self, nx): 
        nx.reset()
        x = nx.eval_debug()
        ny = json_loads(json_dumps(nx))
        y = ny.eval_debug()
        print(type(x))
        if isinstance(x, np.ndarray):
            self.assertEqual(x.dtype, y.dtype)
            self.assertEqual(x.shape, y.shape) 
            self.assertTrue((x==y).all())
        elif isinstance(x, torch.Tensor):
            self.assertEqual(x.dtype, y.dtype)
            self.assertEqual(x.shape, y.shape) 
            self.assertTrue((x==y).all())
        else:
            self.assertEqual(x, y)
        self.assertEqual(nx.debug_info, ny.debug_info)

    def reproduce_literal(self, n): 
        x = n.r
        y = json_loads(json_dumps(n)).r
        if isinstance(x, np.ndarray):
            self.assertEqual(x.dtype, y.dtype)
            self.assertEqual(x.shape, y.shape)             
            return self.assertTrue((x==y).all())
        return self.assertEqual(x, y)


    def test6(self):
        from znode.torch import ŋto_xcoords, ŋto_ycoords
        endpoint = False
        dtype = torch.float64
        n = ŋto_xcoords(10, 10, 0, 10, endpoint, dtype)
        self.reproduce(n)

if __name__ == '__main__':
    unittest.main()
    

