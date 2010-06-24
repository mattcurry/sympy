from sympy.physics.hilbert import l2, L2, FockSpace, TensorProductHilbertSpace, DirectSumHilbertSpace, DirectPowerHilbertSpace

from sympy import Interval, oo, Symbol

def test_l2_int():
    s1 = l2(2)
    s2 = l2(2)
    assert isinstance(s1, l2)
    assert s1.dimension == 2
    assert s1 == s2
    
def test_l2_oo():
    s2 = l2(oo)
    s3 = l2(oo)
    assert isinstance(s2, l2)
    assert s2.dimension == oo
    assert s2 == s3

def test_l2_symbol():
    x = Symbol('x')
    s3 = l2(x)
    s4 = l2(x)
    assert isinstance(s3, l2)
    assert s3.dimension == x
    assert s3 == s4

def test_L2_int():
    b1 = L2(Interval(-42, 42))
    b2 = L2(Interval(-42, 42))
    assert isinstance(b1, L2)
    assert b1.dimension == oo
    assert b1.interval == Interval(-42, 42)
    assert b1 == b2

def test_L2_oo():
    b2 = L2(Interval(-oo, oo))
    b3 = L2(Interval(-oo, oo))
    assert isinstance(b2, L2)
    assert b2.dimension == oo
    assert b2.interval == Interval(-oo, oo)
    assert b2 == b3

def test_L2_symbol():
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)
    b3 = L2(Interval(x, y))
    b4 = L2(Interval(x, y))
    assert isinstance(b3, L2)
    assert b3.dimension == oo
    assert b3.interval == Interval(x, y)
    assert b3 == b4

def test_FockSpace():
    f1 = FockSpace()
    f2 = FockSpace()
    assert isinstance(f1, FockSpace)
    assert f1.dimension == oo
    assert f1 == f2

def test_TensorProductHilbertSpace_l2_int():
    s1 = l2(2)
    s2 = l2(42)
    s3 = s1*s2
    assert isinstance(s3, TensorProductHilbertSpace)
    assert s3.dimension == 84   #(2*42)

def test_TensorProductHilbertSpace_l2_oo():
    s1 = l2(oo)
    s2 = l2(oo)
    s3 = s1*s2
#    assert isinstance(s3, TensorProductHilbertSpace)
    assert s3.dimension == oo

def test_TensorProductHilbertSpace_l2_symbol():
    x = Symbol('x')
    y = Symbol('y')
    s1 = l2(x)
    s2 = l2(y)
    s3 = s1*s2
    assert isinstance(s3, TensorProductHilbertSpace)
    assert s3.dimension == x*y

def test_TensorProductHilbertSpace_L2_int():
    b1 = L2(Interval(-42, 42))
    b2 = L2(Interval(-21, 21))
    b3 = b1*b2
    assert isinstance(b3, TensorProductHilbertSpace)
    assert b3.dimension == oo

def test_TensorProductHilbertSpace_L2_oo():
    b1 = L2(Interval(-oo, oo))
    b2 = L2(Interval(-oo, oo))
    b3 = b1*b2
#    assert isinstance(b3, TensorProductHilbertSpace)
    assert b3.dimension == oo

def test_TensorProductHilbertSpace_L2_symbol():
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)
    q = Symbol('q', real = True)
    p = Symbol('p', real = True)
    b1 = L2(Interval(x, y))
    b2 = L2(Interval(q, p))
    b3 = b1*b2
    assert isinstance(b3, TensorProductHilbertSpace)
    assert b3.dimension == oo

def test_TensorProductHilbertSpace_FockSpace():
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1*f2
#    assert isinstance(f3, TensorProductHilbertSpace)
    assert f3.dimension == oo

def test_TensorProductHilbertSpace_mixed():
    s1 = l2(2)
    s2 = l2(42)
    s3 = s1*s2
    s4 = l2(oo)
    s5 = l2(oo)
    s6 = s4*s5
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)
    s7 = l2(x)
    s8 = l2(x)
    s9 = s7*s8
    b1 = L2(Interval(-42, 42))
    b2 = L2(Interval(-21, 21))
    b3 = b1*b2
    b4 = L2(Interval(-oo, oo))
    b5 = L2(Interval(-oo, oo))
    b6 = b4*b5
    q = Symbol('q', real = True)
    p = Symbol('p', real = True)
    b7 = L2(Interval(x, y))
    b8 = L2(Interval(q, p))
    b9 = b7*b8
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1*f2
    true_test = s3*s6*s9*b3*b6*b9*f3
    assert isinstance(true_test, TensorProductHilbertSpace)
    assert true_test.dimension == oo

def test_DirectSumHilbertSpace_l2_int():
    s1 = l2(2)
    s2 = l2(42)
    s3 = s1+s2
    assert isinstance(s3, DirectSumHilbertSpace)
    assert s3.dimension == 44   #(2+42)

def test_DirectSumHilbertSpace_l2_oo():
    s1 = l2(oo)
    s2 = l2(oo)
    s3 = s1+s2
    assert isinstance(s3, DirectSumHilbertSpace)
    assert s3.dimension == oo

def test_DirectSumHilbertSpace_l2_symbol():
    x = Symbol('x')
    y = Symbol('y')
    s1 = l2(x)
    s2 = l2(y)
    s3 = s1+s2
    assert isinstance(s3, DirectSumHilbertSpace)
    assert s3.dimension == x+y

def test_DirectSumHilbertSpace_L2_int():
    b1 = L2(Interval(-42, 42))
    b2 = L2(Interval(-21, 21))
    b3 = b1+b2
    assert isinstance(b3, DirectSumHilbertSpace)
    assert b3.dimension == oo

def test_DirectSumHilbertSpace_L2_oo():
    b1 = L2(Interval(-oo, oo))
    b2 = L2(Interval(-oo, oo))
    b3 = b1+b2
    assert isinstance(b3, DirectSumHilbertSpace)
    assert b3.dimension == oo

def test_DirectSumHilbertSpace_L2_symbol():
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)
    q = Symbol('q', real = True)
    p = Symbol('p', real = True)
    b1 = L2(Interval(x, y))
    b2 = L2(Interval(q, p))
    b3 = b1+b2
    assert isinstance(b3, DirectSumHilbertSpace)
    assert b3.dimension == oo

def test_DirectSumHilbertSpace_FockSpace():
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1+f2
    assert isinstance(f3, DirectSumHilbertSpace)
    assert f3.dimension == oo

def test_DirectSumHilbertSpace_mixed():
    s1 = l2(2)
    s2 = l2(42)
    s3 = s1+s2
    s4 = l2(oo)
    s5 = l2(oo)
    s6 = s4+s5
    x = Symbol('x', real = True)
    y = Symbol('y', real = True)
    s7 = l2(x)
    s8 = l2(x)
    s9 = s7+s8
    b1 = L2(Interval(-42, 42))
    b2 = L2(Interval(-21, 21))
    b3 = b1+b2
    b4 = L2(Interval(-oo, oo))
    b5 = L2(Interval(-oo, oo))
    b6 = b4+b5
    q = Symbol('q', real = True)
    p = Symbol('p', real = True)
    b7 = L2(Interval(x, y))
    b8 = L2(Interval(q, p))
    b9 = b7+b8
    f1 = FockSpace()
    f2 = FockSpace()
    f3 = f1+f2
    true_test = s3+s6+s9+b3+b6+b9+f3
    assert isinstance(true_test, DirectSumHilbertSpace)
    assert true_test.dimension == oo

def test_DirectPowerHilbertSpace_l2_int():
    s1 = l2(5)
    s2 = s1*s1
    s3 = s1*s1*s1
    s4 = s1**2
    s5 = s1**3
    assert isinstance(s2, DirectPowerHilbertSpace)
    assert isinstance(s3, DirectPowerHilbertSpace)
    assert isinstance(s4, DirectPowerHilbertSpace)
    assert isinstance(s5, DirectPowerHilbertSpace)
    assert s2 == s4
    assert s3 == s5
    assert s4.dimension == s2.dimension == 25  #(5**2)
    assert s5.dimension == s3.dimension == 125 #(5**3)
    assert s4.base == s2.base == l2(5)
    assert s4.exp == s4.exp == 2
    assert s5.base == s3.base == l2(5)
    assert s5.exp == s3.exp == 3
