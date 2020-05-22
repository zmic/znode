import unittest
import json
import numpy as np
import znode

def json_dumps(n):
    return json.dumps(n.dump())

def json_loads(s):
    return znode.load(json.loads(s))

class znode_test1(unittest.TestCase):

    def reproduce(self, n): 
        x = n.eval()
        y = json_loads(json_dumps(n)).eval()
        if isinstance(x, np.ndarray):
            return self.assertTrue((x==y).all())
        return self.assertEqual(x, y)

    def reproduce_literal(self, n): 
        x = n.r
        y = json_loads(json_dumps(n)).r
        if isinstance(x, np.ndarray):
            return self.assertTrue((x==y).all())
        return self.assertEqual(x, y)


    def test0(self):    
        from znode import ŋintegers, ŋint, ŋtuple, ŋnp_array, ŋtuple_literal

        n = ŋtuple()
        x = n.eval()
        self.assertEqual(x, ())
        n = ŋtuple(1,2,3)
        self.assertEqual(str(n), 'ŋtuple(ŋint(1), ŋint(2), ŋint(3))')
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
        n3 = n2.index[-1]
        self.assertEqual(n3.eval(), 3)
        n3 = n2.index[-1]
        self.reproduce(n3)

        n = ŋtuple_literal(())
        self.assertEqual(n.r, ())
        self.reproduce_literal(n)
        n = ŋtuple_literal((1,2,3))
        self.assertEqual(str(n),'ŋtuple_literal((1, 2, 3))')
        self.assertEqual(n.r, (1,2,3))
        self.reproduce_literal(n)
        #n = ŋtuple_literal((1,2,(3,(),(3,))))
        #self.reproduce_literal(n)

        a = ŋint(1)
        with self.assertRaises(TypeError):
            a[0] = 1
        b = ŋint(2)

        n = ŋtuple(a+b,a-b,a*b)
        self.reproduce(n)
        self.assertEqual(n.r, (3,-1, 2))
        
        n = ŋtuple(a+b,a-b,a*b)
        n = n.index[1]
        self.reproduce(n)
        self.assertEqual(n.r, -1)

    def test0b(self):    
        from znode import ŋintegers, ŋrg_MT19937, ŋint, ŋtuple, ŋrandint, ŋnp_RandomState

        nr = ŋrg_MT19937(1200)
        B = ŋintegers(nr,0,8,(3,4))*np.pi/2
        n = B.slice[0,:] * 2       
        self.reproduce(n)
        
        n = B.slice_assign[0,:,0]
        self.reproduce(n)
        self.assertEqual(n.r[0,0],0)

        n = n.astype(np.int).astype(np.float)
        
        n1 = n.astype(np.int).astype(np.float).astype('uint8')
        self.reproduce(n)

        nr = ŋrg_MT19937(1201)
        B = ŋintegers(nr,1,8,(2,4))*np.pi/2
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[1,2:3,50]
        self.reproduce(B)
        #print(B.r)

        nrnd = ŋnp_RandomState(32)
        B = ŋrandint(nr,1,8,(2,4))*np.pi/2
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[0,0:1,50]
        B = B.slice_multiply[1,2:3,50]
        #B.eval()
        #print(B.r)

    def test0c(self):    
        from znode import ŋintegers, ŋint, ŋtuple, ŋnp_array, ŋtuple_literal, ŋslice
        a = ŋnp_array(((1,2),(3,4)), np.float32)
        self.reproduce(a)
        
        a = ŋnp_array(([1,2],[3,4]), np.float32)
        self.reproduce(a)        
        with self.assertRaises(TypeError):
            a = ŋnp_array([(1,2),(3,4)], np.float32)

        n = ŋslice(0,1,None)
        self.assertEqual(n.eval(), slice(0,1,None))
        self.assertEqual(str(n), 'ŋslice(ŋint(0), ŋint(1), ŋNone(None))')
        
        n = a.slice[1,0]
        self.assertEqual(str(n), "ŋnp_slice(ŋnp_array(ŋtuple_literal(([1, 2], [3, 4])), ŋndtype(ŋstr('float32'))), ŋtuple(ŋint(1), ŋint(0)))")
        self.assertEqual(n.eval(), 3)

        n = a.slice[1,0]
        self.reproduce(n)      

        n = a.slice[1,:]
        self.reproduce(n)      
    
    def test1(self):    
        from znode import ŋstandard_normal, ŋrg_MT19937, ŋintegers, ŋint, ŋtuple
    
        n = ŋstandard_normal(ŋrg_MT19937(ŋint(12)),(3,4))
        x = n.eval()
        self.assertAlmostEqual(x[0][0], -0.48977262 )
        x = n.dump()
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [(3, 4)]], ['ŋstandard_normal', [1, 2]]])
        x = json.dumps(n.dump())
        #self.assertEqual(x, r'[["\u014bint", [12]], ["\u014brg_MT19937", [0]], ["\u014btuple", [[3, 4]]], ["\u014bstandard_normal", [1, 2]]]')
        x = json.loads(json.dumps(n.dump()))
        #self.assertEqual(x, [['ŋint', [12]], ['ŋrg_MT19937', [0]], ['ŋtuple', [[3, 4]]], ['ŋstandard_normal', [1, 2]]])
        n2 = json_loads(json_dumps(n))
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
        self.reproduce(n)
        x = n.r
        self.assertEqual(x[0][1][1],1)
        self.assertEqual(x.shape, (2,3,4))

        n1 = ŋndtype(np.float32)
        self.assertEqual(str(n1),"ŋndtype(ŋstr('float32'))")
        self.reproduce(n1)
        n2 = ŋndtype("float32")
        self.assertEqual(str(n2),"ŋndtype(ŋstr('float32'))")
        self.reproduce(n2)

        n = ŋnp_indices((3,4), np.float32)
        x = n.eval()
        self.assertEqual(x[1][1][3],3)
        self.assertEqual(x.dtype,np.float32)
        n = ŋnp_indices((3,4), np.float32)
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

    def test4(self):    
        from znode import ŋintegers, ŋrg_MT19937, ŋint, ŋtuple, ŋrandint, ŋnp_RandomState, ŋnp_transpose, ŋnp_indices, ŋnormal_int
        nrnd2 = ŋrg_MT19937(12)
        n = ŋintegers(nrnd2, 0, 100)            
        self.assertEqual(type(n.eval()), np.int64)

        i = ŋintegers(nrnd2, 5, 6)
        nxy = (1/i)
        self.assertEqual(nxy.eval(), 0.2)

        nxy = ŋnp_transpose(ŋnp_indices((i,i)), (1,2,0))
        #print(nxy.eval())
        nxy = (1/i)*(nxy+0.5)
        #print(nxy.eval())

        for i in range(10):
            n = ŋnormal_int(nrnd2, 3)
            n.eval()

        rs = ŋnp_RandomState(4)
        a = ŋrandint(rs, 0, 10, dtype=np.int32)
        self.reproduce(a)

    def test5(self):
        L = [['ŋint', [800]], ['ŋint', [800]], ['ŋfloat', [-14.24099368720711]], ['ŋfloat', [14.24099368720711]], ['ŋfloat', [-14.24099368720711]], ['ŋfloat', [14.24099368720711]], ['ŋbool', [False]], ['ŋstr', ['dtype']], ['ŋstr', ['float64']], ['ŋndtype', [8]], ['ŋkwarg', [7, 9]], ['ŋcanvas', [0, 1, 2, 3, 4, 5, 6, 10]], ['ŋint', [0]], ['ŋnp_slice', [11, 12]], ['ŋnp_tan', [13]], ['ŋstr', ['int64']], ['ŋndtype', [15]], ['ŋnp_astype', [14, 16]], ['ŋint', [1]], ['ŋint', [1]], ['ŋnp_slice', [11, 19]], ['ŋnp_tan', [20]], ['ŋstr', ['int64']], ['ŋndtype', [22]], ['ŋnp_astype', [21, 23]], ['ŋnp_abs', [24]], ['ŋnp_add', [18, 25]], ['ŋnp_remainder', [17, 26]], ['ŋstr', ['float64']], ['ŋndtype', [28]], ['ŋnp_astype', [27, 29]], ['ŋint', [1]], ['ŋnp_slice', [11, 31]], ['ŋstr', ['int64']], ['ŋndtype', [33]], ['ŋnp_astype', [32, 34]], ['ŋint', [1]], ['ŋstr', ['int64']], ['ŋndtype', [37]], ['ŋnp_astype', [14, 38]], ['ŋnp_abs', [39]], ['ŋnp_add', [36, 40]], ['ŋnp_remainder', [35, 41]], ['ŋstr', ['float64']], ['ŋndtype', [43]], ['ŋnp_astype', [42, 44]], ['ŋnp_exp', [21]], ['ŋnp_multiply', [45, 46]], ['ŋnp_sin', [47]], ['ŋnp_add', [30, 48]], ['ŋnp_add', [49, 45]], ['ŋnp_sin', [50]], ['ŋnp_isnan', [51]], ['ŋfloat', [0.0]], ['ŋnp_where', [52, 53, 51]], ['ŋfloat', [-1e+300]], ['ŋnp_minimum', [54, 55]], ['ŋfloat', [1e+300]], ['ŋnp_maximum', [56, 57]], ['ŋnp_min', [58]], ['ŋnp_max', [58]], ['ŋtuple', [58, 59, 60]]]
        from znode import load
        n = load(L)
        K = n.eval_symbolic()


if __name__ == '__main__':
    unittest.main()
    

