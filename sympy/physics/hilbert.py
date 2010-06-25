"""
Hilbert spaces for quantum mechanics [1].

References
==========

[1] http://en.wikipedia.org/wiki/Hilbert_space
"""

from sympy import Expr, Interval, oo, sympify

class HilbertSpace(Expr):
    """
    An abstract Hilbert space for quantum mechanics.

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
        return DirectPowerHilbertSpace(self, other)

    def __contains__(self, other):
        """Is the operator or state in this Hilbert space."""
        hs = other.hilbert_space
        if hs == self:
            return True
        else:
            return False

class l2(HilbertSpace):
    """
    l2 Hilbert space of any dimension.

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

    def _sympyrepr(self, printer, *args):
        return "l2(%s)" % printer._print(self.dimension, *args)

    def _sympystr(self, printer, *args):
        return "l2(%s)" % printer._print(self.dimension, *args)

class L2(HilbertSpace):
    """
    The Hilbert space of square integrable functions on an interval.

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

    def _sympyrepr(self, printer, *args):
        return "L2(%s)" % printer._print(self.interval, *args)

    def _sympystr(self, printer, *args):
        return "L2(%s)" % printer._print(self.interval, *args)

class FockSpace(HilbertSpace):
    """
    The Hilbert space for second quantization and field theory.

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

    def _sympyrepr(self, printer, *args):
        return "FockSpace()"

    def _sympystr(self, printer, *args):
        return "FS()"

class TensorProductHilbertSpace(HilbertSpace):
    """
    A direct or tensor product of Hilbert spaces [1].

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
        obj = Expr.__new__(cls, *args, commutative=False)
        return obj

    @classmethod
    def eval(cls, args):
        """Evaluates the direct product."""
        new_args = []
        recall = False
        #flatten arguments
        for arg in args:
            if isinstance(arg, TensorProductHilbertSpace):
                new_args.extend(arg.args)
                recall = True
            elif isinstance(arg, (HilbertSpace, DirectPowerHilbertSpace)):
                new_args.append(arg)
            else:
                raise TypeError('Hilbert spaces can only be multiplied by other Hilbert spaces: %r' % arg)
        #combine like arguments into direct powers
        comb_args = []
        prev_arg = None
        for new_arg in new_args:
            if prev_arg != None:
                if isinstance(new_arg, DirectPowerHilbertSpace) and isinstance(prev_arg, DirectPowerHilbertSpace) and new_arg.base == prev_arg.base:
                    prev_arg = new_arg.base**(new_arg.exp+prev_arg.exp)
                elif isinstance(new_arg, DirectPowerHilbertSpace) and new_arg.base == prev_arg:
                    prev_arg = prev_arg**(new_arg.exp+1)
                elif isinstance(prev_arg, DirectPowerHilbertSpace) and new_arg == prev_arg.base:
                    prev_arg = new_arg**(prev_arg.exp+1)
                elif new_arg == prev_arg:
                    prev_arg = new_arg**2
                else:
                    comb_args.append(prev_arg)
                    prev_arg = new_arg
            elif prev_arg == None:
                prev_arg = new_arg
        comb_args.append(prev_arg)
        if recall:
            return TensorProductHilbertSpace(*comb_args)
        elif len(comb_args) == 1:
            return DirectPowerHilbertSpace(comb_args[0].base, comb_args[0].exp)
        else:
            return None

    def _eval_subs(self, old, new):
        r = self.__class__(*[arg.subs(old, new) for arg in self.args])
        return r

    @property
    def dimension(self):
        arg_list = [arg.dimension for arg in self.args]
        if oo in arg_list:
            return oo
        else:
            return reduce(lambda x,y: x*y, arg_list)

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

    def _sympyrepr(self, printer, *args):
        spaces_reprs = self._spaces_printer(printer, *args)
        return "TensorProductHilbertSpace(%s)" % ','.join(spaces_reprs)

    def _sympystr(self, printer, *args):
        spaces_strs = self._spaces_printer(printer, *args)
        return '*'.join(spaces_strs)

class DirectSumHilbertSpace(HilbertSpace):
    """
    A direct sum of Hilbert spaces [1].

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
        obj = Expr.__new__(cls, *args, commutative=False)
        return obj

    @classmethod
    def eval(cls, args):
        """Evaluates the direct product."""
        new_args = []
        recall = False
        #flatten arguments
        for arg in args:
            if isinstance(arg, DirectSumHilbertSpace):
                new_args.extend(arg.args)
                recall = True
            elif isinstance(arg, HilbertSpace):
                new_args.append(arg)
            else:
                raise TypeError('Hilbert spaces can only be summed with other Hilbert spaces: %r' % arg)
        if recall:
            return DirectSumHilbertSpace(*new_args)
        else:
            return None

    def _eval_subs(self, old, new):
        r = self.__class__(*[arg.subs(old, new) for arg in self.args])
        return r

    @property
    def dimension(self):
        arg_list = [arg.dimension for arg in self.args]
        if oo in arg_list:
            return oo
        else:
            return reduce(lambda x,y: x+y, arg_list)

    @property
    def description(self):
        return "A direct sum Hilbert space."

    @property
    def spaces(self):
        """A tuple of the Hilbert spaces in this direct sum."""
        return self.args

    def _sympyrepr(self, printer, *args):
        spaces_reprs = [printer._print(arg, *args) for arg in self.args]
        return "DirectSumHilbertSpace(%s)" % ','.join(spaces_reprs)

    def _sympystr(self, printer, *args):
        spaces_strs = [printer._print(arg, *args) for arg in self.args]
        return '+'.join(spaces_strs)

class DirectPowerHilbertSpace(HilbertSpace):
    """
    An exponentiated (iterated tensor/direct product) Hilbert space [1].

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
        return Expr.__new__(cls, *r, commutative=False)

    @classmethod
    def eval(cls, args):
        new_args = args[0], sympify(args[1])
        exp = new_args[1]
        #simplify hs**1 -> hs
        if exp == 1:
            return args[0]
        #simplify hs**0 -> 1
        if exp == 0:
            return sympify(1)
        #check (and allow) for hs**(x+42+y...) case
        if len(exp.atoms()) == 1:
            if not (exp.is_Integer and exp >= 0 or exp.is_Symbol):
                raise ValueError('Hilbert spaces can only be raised to positive integer powers or symbols: %r' % exp)
        for power in exp.atoms():
            if not (power.is_Integer or power.is_Symbol):
                raise ValueError('Hilbert spaces can only be raised to positive integer powers or symbols: %r' % exp)
        return new_args

    def _eval_subs(self, old, new):
        r = self.__class__(self.base.subs(old, new), self.exp.subs(old, new))
        return r

    @property
    def base(self):
        return self.args[0]

    @property
    def exp(self):
        return self.args[1]

    @property
    def dimension(self):
        if self.base.dimension == oo:
            return oo
        else:
            return self.base.dimension**self.exp

    @property
    def description(self):
        return "An exponentiated Hilbert space."

#    def as_product(self):
#        args = int(self.exp)*[self.base]
#        return TensorProductHilbertSpace(*args)

    def _sympyrepr(self, printer, *args):
        return "DirectPowerHilbertSpace(%s,%s)" % (printer._print(self.base, *args), printer._print(self.exp, *args))

    def _sympystr(self, printer, *args):
        return "%s**(%s)" % (printer._print(self.base, *args), printer._print(self.exp, *args))
