"""
An example of 5-qubit error correcting code is given.
"""

from sympy.physics.quantum.gate import H, X, Z, CNOT
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.applyops import apply_operators
from sympy.printing.pretty import pprint
from sympy.physics.quantum.circuitplot import circuit_plot
from sympy.core.numbers import Rational

print "Create codeword operators:"
print ""
print "M0:"
M0 = Z(1)*X(2)*X(3)*Z(4)
pprint(M0)
print ""
print "M1:"
M1 = Z(2)*X(3)*X(4)*Z(0)
pprint(M1)
print ""
print "M2:"
M2 = Z(3)*X(4)*X(0)*Z(1)
pprint(M2)
print ""
print "M3:"
M3 = Z(4)*X(0)*X(1)*Z(2)
pprint(M3)
print ""

print "Apply these operators to create codeword states:"
print ""
print "Zero:"
zero = Rational(1,4)*(1+M0)*(1+M1)*(1+M2)*(1+M3)*Qubit('00000')
pprint(zero)
print ""
print "Apply the operators:"
pprint(apply_operators(zero))
print ""
print "One:"
one = Rational(1,4)*(1+M0)*(1+M1)*(1+M2)*(1+M3)*Qubit('11111')
pprint(one)
print ""
print "Apply the operators:"
pprint(apply_operators(one))
print ""

print "Create encoding circuit:"
print ""
# CNOT <=> Controlled-Not Gate
# H <=> Hadamard Gate
# Z <=> Z Gate
qbec = H(3)*H(4)*CNOT(2, 0)*CNOT(3, 0)*CNOT(4, 0)*H(1)*H(4)*CNOT(2, 1)*\
        CNOT(4, 1)*H(2)*CNOT(3, 2)*CNOT(4, 2)*H(3)*H(4)*CNOT(4, 3)*Z(4)*H(4)*Z(4)
circuit_plot(qbec, nqubits=5)
