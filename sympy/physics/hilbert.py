"""Hilbert spaces for quantum mechanics [1].

References
==========

[1] http://en.wikipedia.org/wiki/Hilbert_space
"""

from sympy import Expr, Interval, oo, sympify

class HilbertSpace(Expr):
    """An abstract Hilbert space for quantum mechanics.

    Examples
    ========
    
    """

    description = 'General abstract Hilbert space.'

    def __new__(cls):
        obj = Expr.__new__(cls, commutative=False)
        return obj

    @property
    def dimension(self):
        """Return the Hilbert dimension of the space."""
        raise NotImplementedError('This Hilbert space has no dimension.')

    def __add__(self, other):
        return DirectSumHilbertSpace(self, other)

    def __radd__(self, other):
        return DirectSumHilbertSpace(other, self)

    def __mul__(self, other):
        return TensorProductHilbertSpace(self, other)

    def __rmul__(self, other):
        return TensorProductHilbertSpace(other, self)

    def __pow__(self, other, mod=None):
        if mod is not None:
            raise ValueError('The third argument to __pow__ is not supported for Hilbert spaces.')
        times = sympify(other)
        if not (times.is_Integer and times >= 0):
            raise ValueError('Hilbert spaces can only be raised to positive integer powers: %r' % times)
        args = int(times)*[self]
        return TensorProductHilbertSpace(*args)

    def __contains__(self, other):
        """Is the operator or state in this Hilbert space."""
        hs = other.hilbert_space
        if hs == self:
            return True
        else:
            return False

class l2(HilbertSpace):
    """l2 Hilbert space of any dimension.

    l2 (little-ell-two) is a Hilbert space of complex valued vectors. The
    number of components of the vectors in the space is the dimension of 
    the Hilbert space. l2 can have a dimension of infinity, but it is a 
    countable infinity (vector components labeled by the natural numbers).

    A classic example of an l2 space is spin-1/2, which is l2(2). For spin-s,
    the space is l2(2*s+1). Quantum computing with N qubits is done with
    the direct product space l2(2)**N.

    Examples
    ========

    """

    def __new__(cls, dimension):
        dimension = sympify(dimension)
        if not (dimension.is_Integer or dimension is oo or dimension.is_Symbol):
            raise TypeError('l2 dimension must be an integer, oo or a Symbol: %r' % dimension)
        obj = Expr.__new__(cls, dimension, commutative=False)
        return obj

    def _eval_subs(self, old, new):
        r = self.__class__(self.args[0].subs(old, new))
        return r

    @property
    def dimension(self):
        return self.args[0]

    @property
    def description(self):
        return 'Hilbert space of length %s complex valued vectors.' % str(self.dimension)

    def _sympyrepr_(self, printer, *args):
        return "l2(%s)" % printer._print(self.dimension, *args)

    def _sympystr_(self, printer, *args):
        return "l2(%s)" % printer._print(self.dimension, *args)

class L2(HilbertSpace):
    """The Hilbert space of square integrable functions on an interval.

    L2 (big-ell-two) has a dimension of infinity. L2 is different than
    l2(oo) because the elements of L2 have an uncountable number of components,
    that is, they are function.

    Examples
    ========
    """

    def __new__(cls, interval):
        if not isinstance(interval, Interval):
            raise TypeError('L2 interval must be an Interval instance: %r' % interval)
        obj = Expr.__new__(cls, interval, commutative=False)
        return obj

    def _eval_subs(self, old, new):
        r = self.__class__(self.args[0].subs(old, new))
        return r

    @property
    def dimension(self):
        return oo

    @property
    def interval(self):
        return self.args[0]

    @property
    def description(self):
        return 'Hilbert space of square integrable functions on the interval %s.' % str(self.interval)

    def _sympyrepr_(self, printer, *args):
        return "L2(%s)" % printer._print(self.interval, *args)

    def _sympystr_(self, printer, *args):
        return "L2(%s)" % printer._print(self.interval, *args)

class FockSpace(HilbertSpace):
    """The Hilbert space for second quantization and field theory.

    Technically, this Hilbert space is a symmetrized/anti-symmetrized infinite
    direct sum of direct products of single particle Hilbert spaces [1]. This
    is a mess, so we have a class to represent it directly.

    Examples
    ========

    References
    ==========

    [1] http://en.wikipedia.org/wiki/Fock_space
    """

    def __new__(cls):
        obj = Expr.__new__(cls, commutative=False)
        return obj

    @property
    def dimension(self):
        return oo

    @property
    def description(self):
        return 'Hilbert space of Fock space.'

    def _sympyrepr_(self, printer, *args):
        return "FockSpace(%s)" % printer._print(self.interval, *args)

    def _sympystr_(self, printer, *args):
        return "FS(%s)" % printer._print(self.interval, *args)

class TensorProductHilbertSpace(HilbertSpace):
    """A direct or tensor product of Hilbert spaces [1].

    Examples
    ========

    References
    ==========

    [1] http://en.wikipedia.org/wiki/Hilbert_space#Tensor_products
    """

    def __new__(cls, *args):
        r = cls.eval(args)
        if isinstance(r, Expr):
            return r
        obj = Expr.__new__(cls, *args)
        return obj

    @classmethod
    def eval(cls, args):
        """Evaluates the direct product."""
        new_args = []
        recall = False
        for arg in args:
            if isinstance(arg, TensorProductHilbertSpace):
                new_args.extend(arg.args)
                recall = True
            elif isinstance(arg, HilbertSpace):
                new_args.append(arg)
            else:
                raise TypeError('Hilbert spaces can only be multiplied by other Hilbert spaces: %r' % arg)
        if recall:
            return TensorProductHilbertSpace(*new_args)
        else:
            return None

    def _eval_subs(self, old, new):
        r = self.__class__(*[arg.subs(old, new) for arg in self.args])
        return r

    @property
    def dimension(self):
        return reduce(lambda x,y: x*y, [arg.dimension for arg in self.args])

    @property
    def description(self):
        return "A direct product Hilbert space."

    @property
    def spaces(self):
        """A tuple of the Hilbert spaces in this tensor product."""
        return self.args

    def _spaces_printer(self, printer, *args):
        spaces_strs = []
        for arg in self.args:
            s = printer._print(arg, *args)
            if isinstance(arg, DirectSumHilbertSpace):
                s = '(%s)' % s
            spaces_strs.append(s)
        return spaces_strs

    def _sympyrepr_(self, printer, *args):
        spaces_reprs = self._spaces_printer(printer, *args)
        return "TensorProductHilbertSpace(%s)" % ','.join(spaces_reprs)

    def _sympystr_(self, printer, *args):
        spaces_strs = self._spaces_printer(printer, *args)
        return '*'.join(spaces_strs)

class DirectSumHilbertSpace(HilbertSpace):
    """A direct sum of Hilbert spaces [1].

    Examples
    ========

    References
    ==========

    [1] http://en.wikipedia.org/wiki/Hilbert_space#Direct_sums
    """
    def __new__(cls, *args):
        r = cls.eval(args)
        if isinstance(r, Expr):
            return r
        obj = Expr.__new__(cls, *args)
        return obj

    @classmethod
    def eval(cls, args):
        """Evaluates the direct product."""
        new_args = []
        recall = False
        for arg in args:
            if isinstance(arg, DirectSumHilbertSpace):
                new_args.extend(arg.args)
                recall = True
            elif isinstance(arg, HilbertSpace):
                new_args.append(arg)
            else:
                raise TypeError('Hilbert spaces can only be multiplied by other Hilbert spaces: %r' % arg)
        if recall:
            return DirectSumHilbertSpace(*new_args)
        else:
            return None

    def _eval_subs(self, old, new):
        r = self.__class__(*[arg.subs(old, new) for arg in self.args])
        return r

    @property
    def dimension(self):
        return reduce(lambda x,y: x+y, [arg.dimension for arg in self.args])

    @property
    def description(self):
        return "A direct sum Hilbert space."

    @property
    def spaces(self):
        """A tuple of the Hilbert spaces in this direct sum."""
        return self.args

    def _sympyrepr_(self, printer, *args):
        spaces_reprs = [printer._print(arg, *args) for arg in self.args]
        return "DirectSumHilbertSpace(%s)" % ','.join(spaces_reprs)

    def _sympystr_(self, printer, *args):
        spaces_strs = [printer._print(arg, *args) for arg in self.args]
        return '+'.join(spaces_strs)
