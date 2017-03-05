
from hypothesis import given, strategies as st, assume
from math import isclose
from unittest import TestCase, skip
import numpy as np

from fuzzy.classes import Domain, Set
from fuzzy import functions as fun
from fuzzy import hedges
from fuzzy import combinators as combi
import fuzzy.rules as ru

class Test_Functions(TestCase):
    @given(st.floats(allow_nan=False))
    def test_noop(self, x):
        f = fun.noop()
        assert f(x) == x

    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_inv(self, x):
        assume(0 <= x <= 1)
        f = fun.inv(fun.noop())
        assert isclose(f(f(x)), x, abs_tol=1e-16)

    @given(st.floats(allow_nan=False, allow_infinity=False), 
           st.floats(allow_nan=False, allow_infinity=False))
    def test_constant(self, x, c):
        f = fun.constant(c)
        assert f(x) == c


    @given(st.floats(allow_nan=False),
            st.floats(min_value=0, max_value=1),
            st.floats(min_value=0, max_value=1))
    def test_alpha(self, x, lower, upper):
        assume(lower < upper)
        f = fun.alpha(lower, upper, fun.noop())
        if x <= lower:
            assert f(x) == lower
        elif x >= upper:
            assert f(x) == upper
        else:
            assert f(x) == x
            
    @given(st.floats(allow_nan=False),
            st.floats(min_value=0, max_value=1))
    def test_normalize(self, x, height):
        assume(0 < height)
        f = fun.normalize(height, fun.alpha(0, height, fun.R(0,100)))
        assert (0 <= f(x) <= 1)       

    @given(st.floats(),
           st.floats(),
           st.floats(min_value=0, max_value=1),
           st.floats(min_value=0, max_value=1))
    def test_singleton(self, x, c, no_m, c_m):
        assume(0 <= no_m < c_m <= 1)
        f = fun.singleton(c, no_m=no_m, c_m=c_m)
        assert f(x) == (c_m if x == c else no_m)
    
    
    @given(st.floats(allow_nan=False, allow_infinity=False),
          st.floats(allow_nan=False, allow_infinity=False),
          st.floats(allow_nan=False, allow_infinity=False))
    def test_linear(self, x, m, b):
        f = fun.linear(m, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1),
      st.floats(min_value=0, max_value=1))
    def test_bounded_linear(self, x, low, high, c_m, no_m):
        assume(low < high)
        assume(c_m > no_m)
        f = fun.bounded_linear(low, high, c_m=c_m, no_m=no_m)
        assert (0 <= f(x) <= 1)

    @given(st.floats(allow_nan=False),
            st.floats(allow_nan=False, allow_infinity=False),
            st.floats(allow_nan=False, allow_infinity=False))
    def test_R(self, x, low, high):
        assume(low < high)
        f = fun.R(low, high)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
        st.floats(allow_nan=False, allow_infinity=False),
        st.floats(allow_nan=False, allow_infinity=False))
    def test_S(self, x, low, high):
        assume(low < high)
        f = fun.S(low, high)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1),
      st.floats(min_value=0, max_value=1))
    def test_rectangular(self, x, low, high, c_m, no_m):
        assume(low < high)
        f = fun.rectangular(low, high, c_m=c_m, no_m=no_m)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1),
      st.floats(min_value=0, max_value=1))
    def test_triangular(self, x, low, high, c, c_m, no_m):
        assume(low < c < high)
        assume(no_m < c_m)
        f = fun.triangular(low, high, c=c, c_m=c_m, no_m=no_m)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1),
      st.floats(min_value=0, max_value=1))
    def test_trapezoid(self, x, low, c_low, c_high, high, c_m, no_m):
        assume(low < c_low <= c_high < high)
        assume(no_m < c_m)
        f = fun.trapezoid(low, c_low, c_high, high, c_m=c_m, no_m=no_m)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(min_value=0, max_value=1),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1))
    def test_sigmoid(self, x, L, k, x0):
        assume(0 < L <= 1)
        f = fun.sigmoid(L, k, x0)
        assert (0 <= f(x) <= 1)

    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False))
    def test_bounded_sigmoid(self, x, low, high):
        assume(low < high)
        f = fun.bounded_sigmoid(low, high)
        assert (0 <= f(x) <= 1)
    
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False))
    def test_simple_sigmoid(self, x, k):
        f = fun.simple_sigmoid(k)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False))
    def test_triangular_sigmoid(self, x, low, high, c):
        assume(low < c < high)
        f = fun.triangular(low, high, c=c)
        assert (0 <= f(x) <= 1)
    
    @given(st.floats(allow_nan=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(allow_nan=False, allow_infinity=False),
      st.floats(min_value=0, max_value=1))
    def test_gauss(self, x, b, c, c_m):
        assume(0 < b)
        assume(0 < c_m)
        f = fun.gauss(c, b, c_m=c_m)
        assert (0 <= f(x) <= 1)

class Test_Hedges(TestCase):
    @given(st.floats(min_value=0, max_value=1))
    def test_very(self, x):
        s = Set(fun.noop())
        f = hedges.very(s)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_minus(self, x):
        s = Set(fun.noop())
        f = hedges.minus(s)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_plus(self, x):
        s = Set(fun.noop())
        f = hedges.plus(s)
        assert (0 <= f(x) <= 1)


class Test_Combinators(TestCase):
    @given(st.floats(min_value=0, max_value=1))
    def test_MIN(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.MIN(a, b)
        assert (0 <= f(x) <= 1)

    @given(st.floats(min_value=0, max_value=1))
    def test_MAX(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.MAX(a, b)
        assert (0 <= f(x) <= 1)
    
    @given(st.floats(min_value=0, max_value=1))
    def test_product(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.product(a, b)
        assert (0 <= f(x) <= 1)
    
    @given(st.floats(min_value=0, max_value=1))
    def test_bounded_sum(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.bounded_sum(a, b)
        assert (0 <= f(x) <= 1)

    @given(st.floats(min_value=0, max_value=1))
    def test_lukasiewicz_AND(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.lukasiewicz_AND(a, b)
        assert (0 <= f(x) <= 1)

    @given(st.floats(min_value=0, max_value=1))
    def test_lukasiewicz_OR(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.lukasiewicz_OR(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_einstein_product(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.einstein_product(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_einstein_sum(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.einstein_sum(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_hamacher_product(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.hamacher_product(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_hamacher_sum(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.hamacher_sum(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1),
          st.floats(min_value=0, max_value=1))
    def test_lambda_op(self, x, l):
        a = fun.noop()
        b = fun.noop()
        g = combi.lambda_op(l)
        f = g(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1),
          st.floats(min_value=0, max_value=1))
    def test_gamma_op(self, x, g):
        a = fun.noop()
        b = fun.noop()
        g = combi.gamma_op(g)
        f = g(a, b)
        assert (0 <= f(x) <= 1)
        
    @given(st.floats(min_value=0, max_value=1))
    def test_hamacher_sum(self, x):
        a = fun.noop()
        b = fun.noop()
        f = combi.simple_disjoint_sum(a, b)
        assert (0 <= f(x) <= 1)

class Test_Domain(TestCase):
    def test_basics(self):
        d = Domain("d", 0, 10)
        assert d.name == "d"
        assert d.low == 0
        assert d.high == 10
        assert d.res == 1
        x = Set(lambda x: 1)
        d.s = x
        assert d.s == x
        assert d._sets == {"s": x}
        R = d(3)
        assert R == {"s": 1}
        # repr is hard - need to repr sets first :/
        #D = eval(repr(d))
        #assert d == D
        
class Test_Set(TestCase):
    @skip("repr is complicated")
    def test_repr_unassigned(self):
        s1 = Set(fun.noop())
        s2 = eval(repr(s1))
        assert s1 == s2
    
    @given(st.floats(allow_nan=False, allow_infinity=False),
           st.floats(allow_nan=False, allow_infinity=False),
          st.floats(min_value=0.0001, max_value=1))
    def test_eq(self, low, high, res):
        """This also tests Set.array().
        This test can massively slow down hypothesis with even 
        reasonably large/small values.
        """
        assume(low < high)
        # to avoid MemoryError and runs that take forever..
        assume(high - low <= 100)
        D1 = Domain("1", low, high, res=res)
        D1.s1 = Set(fun.bounded_linear(low, high))
        D2 = Domain("2", low, high, res=res)
        D2.s2 = Set(fun.bounded_linear(low, high))
        assert(D1.s1 == D2.s2)
    
    def test_normalized(self):
        D = Domain("d", 0, 10, res=0.1)
        D.s = Set(fun.bounded_linear(3, 12))
        x = D.s.normalized()
        y = x.normalized()
        
        assert (set(D._sets.keys()) == set(["s", "normalized_s", "normalized_normalized_s"]))
        assert x == y
        
    def test_sub_super_set(self):
        D = Domain("d", 0, 10, res=0.1)
        D.s = Set(fun.bounded_linear(3, 12))
        x = D.s.normalized()
        assert (x >= D.s)
        assert (D.s <= x)
        
    def test_complement(self):
        D = Domain("d", 0, 10, res=0.1)
        D.s1 = Set(fun.bounded_linear(3, 12))
        D.s2 = ~~D.s1
        assert all(np.isclose(D.s1.array(), D.s2.array()))
        

class Test_Rules(TestCase):
    @given(st.floats(min_value=0, max_value=1),
           st.floats(allow_infinity=False, allow_nan=False),
           st.floats(allow_infinity=False, allow_nan=False),
           st.floats(min_value=0, max_value=1),
           st.floats(min_value=0, max_value=1))
    def test_rescale(self, x, out_min, out_max, in_min, in_max):
        assume(in_min < in_max)
        assume(in_min <= x <= in_max)
        assume(out_min < out_max)
        f = ru.rescale(out_min, out_max) 
        assert (out_min <= f(x) <= out_max)
        
    @given(st.floats(allow_nan=False),
          st.floats(allow_nan=False))
    def round_partial(self, x, res):
        assert(isclose(x, ru.round_partial(x, res), res=res))