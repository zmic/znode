import unittest
import json
import numpy as np
import znode
import ast


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
        if isinstance(x, np.ndarray):
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

    def test0(self):
        # check if znode.load works without importing the specific nodes
        L = [['ŋint', [1]], ['ŋint', [3]], ['ŋint', [2]], ['ŋsub', [1, 2]], ['ŋadd', [0, 3]]]
        n = znode.load(L)
        self.assertEqual(L, n.dump())
        # check if a new node type dumps/loads.
        from znode.core import node__
        class ŋextra(node__):
            pass
        n = ŋextra(n)
        L = [['ŋint', [1]], ['ŋint', [3]], ['ŋint', [2]], ['ŋsub', [1, 2]], ['ŋadd', [0, 3]], ['ŋextra', [4]]]
        self.assertEqual(L, n.dump())
        self.assertEqual(znode.load(n.dump()).dump(), n.dump())
        K = n.eval_symbolic()
        
    def testa(self):    
        from znode import ŋr_integers, ŋint, ŋtuple, ŋp_array, ŋlist_literal

        n = ŋtuple()
        x = n.eval()
        self.assertEqual(x, ())
        n = ŋtuple(1,2,3)
        self.assertEqual(str(n), 'ŋtuple[ŋint(1), ŋint(2), ŋint(3)]')
        x = n.eval()
        self.assertEqual(x, (1,2,3))
        n = ŋtuple(1,2,(3,(),(3,)))
        self.assertEqual(n.eval(), (1, 2, (3, (), (3,))))
        
        
        n = ŋtuple(1,2,(3,(),(3,)))
        self.reproduce(n)

        n = ŋtuple(1,2,3,4,(5,None),None)
        self.reproduce(n)

        n = ŋtuple(1,2,3)
        n2 = n.index[1:4]
        self.assertEqual(n2.eval(), (2,3))
        n2 = n.index[1:4]
        #print(n2)
        self.reproduce(n2)

        n3 = n2.index[-1]
        self.assertEqual(n3.eval(), 3)
        n3 = n2.index[-1]
        self.reproduce(n3)

        n = ŋlist_literal(())
        self.assertEqual(n.r, [])
        self.reproduce_literal(n)
        n = ŋlist_literal((1,2,3))
        self.assertEqual(str(n),'ŋlist_literal([1, 2, 3])')
        self.assertEqual(n.r, [1,2,3])
        self.reproduce_literal(n)
        #n = ŋtuple_literal((1,2,(3,(),(3,))))
        #self.reproduce_literal(n)

        a = ŋint(1)
        #with self.assertRaises(TypeError):
        #    a[0] = 1
        b = ŋint(2)

        n = ŋtuple(a+b,a-b,a*b)
        self.reproduce(n)
        self.assertEqual(n.r, (3,-1, 2))
        
        n = ŋtuple(a+b,a-b,a*b)
        n = n.index[1]
        self.reproduce(n)
        self.assertEqual(n.r, -1)

    def test0b(self):    
        from znode import ŋr_integers, ŋr_MT19937, ŋint, ŋtuple, ŋr_Generator

        nr = ŋr_Generator(ŋr_MT19937(1200))
        B = ŋr_integers(nr,0,8,(3,4))*np.pi/2
        n = B.slice[0,:] * 2       
        self.reproduce(n)
        
        n = B.slice_assign[0,:,0]
        self.reproduce(n)
        self.assertEqual(n.r[0,0],0)

        n = n.astype(np.int32).astype(np.float64)
        
        n1 = n.astype(np.int32).astype(np.float64).astype('uint8')
        self.reproduce(n)

        nr = ŋr_Generator(ŋr_MT19937(1201))
        B = ŋr_integers(nr,1,8,(2,4))*np.pi/2
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[1,2:3,50]
        self.reproduce(B)
        #print(B.r)

    def test0c(self):    
        from znode import ŋint, ŋtuple, ŋp_array, ŋlist_literal, ŋslice
        a = ŋp_array(((1,2),(3,4)), np.float32)
        self.reproduce(a)
        
        a = ŋp_array(([1,2],[3,4]), np.float32)
        self.reproduce(a)        
        #with self.assertRaises(TypeError):
        b = ŋp_array([(1,2),(3,4)], np.float32)
        self.reproduce(b)        

        n = ŋslice(0,1,None)
        self.assertEqual(n.eval(), slice(0,1,None))
        self.assertEqual(str(n), 'ŋslice[ŋint(0), ŋint(1), ŋNone(None)]')
        
        n = a.slice[1,0]
        self.assertEqual(str(n), "ŋp_slice[ŋp_array[ŋlist_literal([[1, 2], [3, 4]]), ŋp_ndtype[ŋstr('float32')]], ŋtuple[ŋint(1), ŋint(0)]]")
        self.assertEqual(n.eval(), 3)

        n = a.slice[1,0]
        self.reproduce(n)      

        n = a.slice[1,:]
        self.reproduce(n)      
    
    def test1(self):    
        from znode import ŋr_standard_normal, ŋr_MT19937, ŋr_Generator, ŋr_integers, ŋint, ŋtuple
    
        n = ŋr_standard_normal(ŋr_Generator(ŋr_MT19937(ŋint(12))),(3,4))
        x = n.eval()
        self.assertAlmostEqual(x[0][0], -0.82183416 )
        x = n.dump()
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [(3, 4)]], ['ŋstandard_normal', [1, 2]]])
        x = json.dumps(n.dump())
        #self.assertEqual(x, r'[["\u014bint", [12]], ["\u014brg_MT19937", [0]], ["\u014btuple", [[3, 4]]], ["\u014bstandard_normal", [1, 2]]]')
        x = json.loads(json.dumps(n.dump()))
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [[3, 4]]], ['ŋstandard_normal', [1, 2]]])
        n2 = json_loads(json_dumps(n))
        x = n2.eval()
        self.assertAlmostEqual(x[0][0], -0.82183416 )

        #self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))))
        #self.assertEqual( "ŋstandard_normal(ŋrg_MT19937(ŋint(12)), ŋtuple((3, 4)))", repr(ŋstandard_normal(ŋrg_MT19937(ŋint(12)), (3, 4))))

        n = ŋr_Generator(ŋr_MT19937(12))
        n = ŋr_integers(n, 0, 10, (4,4))
        self.reproduce(n)

    def test2(self):
        from znode import ŋp_indices, ŋp_ndtype

        n = ŋp_indices((3,4))
        self.reproduce(n)
        x = n.r
        self.assertEqual(x[0][1][1],1)
        self.assertEqual(x.shape, (2,3,4))

        n1 = ŋp_ndtype(np.float32)
        self.assertEqual(str(n1),"ŋp_ndtype[ŋstr('float32')]")
        self.reproduce(n1)
        n2 = ŋp_ndtype("float32")
        self.assertEqual(str(n2),"ŋp_ndtype[ŋstr('float32')]")
        self.reproduce(n2)

        n = ŋp_indices((3,4), np.float32)
        x = n.eval()
        self.assertEqual(x[1][1][3],3)
        self.assertEqual(x.dtype,np.float32)
        n = ŋp_indices((3,4), np.float32)
        self.reproduce(n)

    def test3(self):
        from znode import ŋp_indices, ŋp_transpose, ŋp_concatenate, ŋtuple, ŋp_reshape
        from znode import ŋr_Generator, ŋr_PCG64, ŋr_random
        x = 8
        n = ŋp_transpose(ŋp_indices((x,x)), (1,2,0))
        self.reproduce(n)
        n = n + 0.5
        self.reproduce(n)
        n2 = n*(1/x)
        self.reproduce(n2)
        n1 = (1/x)*n
        self.reproduce(n1)

        n1 = ŋp_reshape(n1, (x*x,2))
        self.reproduce(n1)

        nr = ŋr_Generator(ŋr_PCG64(32))
        n2 = ŋr_random(nr, (x*x,1))
        n2 = n2 / 10
        self.reproduce(n2)
        n1 = ŋp_concatenate((n1, n2), 1)
        self.reproduce(n1)

    def test4(self):    
        from znode import ŋr_integers, ŋr_default_rng, ŋint, ŋtuple, ŋr_integers
        from znode import ŋp_transpose, ŋp_indices, ŋr_normal_int, ŋp_int64
        
        nrnd2 = ŋr_default_rng(12)
        n = ŋr_integers(nrnd2, 0, 100)            
        self.assertEqual(type(n.eval()), np.int64)

        i = ŋr_integers(nrnd2, 5, 6)
        nxy = (1/i)
        self.assertEqual(nxy.eval(), 0.2)

        nxy = ŋp_transpose(ŋp_indices((i,i)), (1,2,0))
        #print(nxy.eval())
        nxy = (1/i)*(nxy+0.5)
        #print(nxy.eval())

        for i in range(10):
            n = ŋr_normal_int(nrnd2, 3)
            n.eval()

        rs = ŋr_default_rng(4)
        a = ŋr_integers(rs, 0, 10, dtype=np.int32)
        self.reproduce(a)
        i = np.int64(3333333333)
        i = i*i
        n = ŋp_int64(i)
        n = n+n
        self.reproduce(n)
    
    def test5(self):
        from znode import ŋr_default_rng, ŋr_exponential, ŋp_array, ŋtuple, ŋlist, ŋp_array_literal
        n = ŋr_exponential(ŋr_default_rng(), 1e20, (2,2,2))
        r = n.eval()
        n2 = ŋp_array(r.tolist())
        self.reproduce(n2)
        n = ŋtuple(1,2,3)
        self.assertEqual(str(n), "ŋtuple[ŋint(1), ŋint(2), ŋint(3)]")
        n = ŋtuple((1,2,3))
        self.assertEqual(str(n), "ŋtuple[ŋtuple[ŋint(1), ŋint(2), ŋint(3)]]")
        n = ŋtuple(r)
        n = ŋp_array_literal(r.astype(np.longdouble))
        n = ŋp_array([[1,2,3],[7,8,9]], dtype=np.uint8)
        self.assertEqual(n.eval().dtype, np.uint8)
        self.reproduce(n)
    
    def test6(self):
        from znode import ŋp_ones,ŋp_cos
        n = ŋp_cos(ŋp_ones((2,2), dtype=np.float64))
        i = np.float64(.6)
        n = n*i

    def test7(self):
        from znode import ŋvariable, ŋp_cos
        n = ŋvariable('n',1)
        n2 = n+ŋp_cos(0)
        n.eval()


if __name__ == '__main__':
    unittest.main()
    

