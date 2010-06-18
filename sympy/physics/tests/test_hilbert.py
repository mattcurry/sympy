from sympy.physics.hilbert import l2, L2, FockSpace, TensorProductHilbertSpace

from sympy import Interval, oo, Symbol 

def test_l2():
    s1 = l2(2)
    s2 = l2(42)
    s3 = l2(oo)
    x = Symbol('x')
    s4 = l2(x)
    assert isinstance(s1, l2)
    assert isinstance(s2, l2)
    assert isinstance(s3, l2)
    assert isinstance(s4, l2)
    assert s1.dimension == 2
    assert s2.dimension == 42
    assert s3.dimension == oo
    assert s4.dimension == x

def test_L2():
    b1 = L2(Interval(-oo, oo))
    b2 = L2(Interval(-42, 42))
    assert isinstance(b1, L2)
    assert isinstance(b2, L2)
    assert b1.dimension == oo
    assert b2.dimension == oo
    assert b1.interval == Interval(-oo, oo)
    assert b2.interval == Interval(-42, 42)

def test_FockSpace():
    f1 = FockSpace()
    assert isinstance(f1, FockSpace)
    assert f1.dimension == oo
    
def test_TensorProductHilbertSpace():
    s1 = l2(2)
    s2 = l2(42)
    s3 = l2(oo)
    x = Symbol('x')
    s4 = l2(x)
    s5 = s1**5
    s6 = s2**2
    s7 = s3**3
    s8 = s4**20
    s9 = s1*s2
    s10 = s1*s4
    b1 = L2(Interval(-oo, oo))
    b2 = L2(Interval(-42, 42))
    b3 = b1*b2
    b4 = b1**17
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1*f2
    p1 = s8*s9*s10*b3*b4*f3
    assert s5.dimension == 32   #(2**5)
    assert s6.dimension == 1764 #(42**2)
    assert s7.dimension == oo
    assert s8.dimension == x**20
    assert s8.spaces == tuple(s8.args)
    assert s9.dimension == 84   #(2*42)
    assert s10.dimension == 2*x
    assert b3.dimension == oo
    assert b4.dimension == oo
    assert f3.dimension == oo
    assert isinstance(p1, TensorProductHilbertSpace)
    assert p1.dimension == oo*x**21

def test_DirectSumHilbertSpace():
    s1 = l2(2)
    s2 = l2(42)
    s3 = l2(oo)
    x = Symbol('x')
    s4 = l2(x)
    s5 = s1**5
    s6 = s2**2
    s7 = s3**3
    s8 = s4**20
    s9 = s1+s2
    s10 = s1+s4
    b1 = L2(Interval(-oo, oo))
    b2 = L2(Interval(-42, 42))
    b3 = b1+b2
    b4 = b1**17
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1+f2
    p1 = s8+s9+s10+b3+b4+f3
    assert s9.dimension == 44
    assert s10.dimension ==  2+x
    assert b3.dimension == oo
    assert p1.dimension == oo+x+x**20
