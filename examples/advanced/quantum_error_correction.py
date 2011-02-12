"""
An example of creating a 5-qubit encoding circuit is given.
"""

from sympy.physics.quantum.gate import H, Z, CNOT
from sympy.physics.quantum.qubit import Qubit
from sympy.physics.quantum.applyops import apply_operators
from sympy.printing.pretty import pprint

print "Create two 5-qubit states:"
print ""
zero = Qubit(0,0,0,0,0)
one = Qubit(1,0,0,0,0)
print zero
print ""
print one
print ""

print "Create encoding circuit:"
print ""
# CNOT <=> Controlled-Not Gate
# H <=> Hadamard Gate
# Z <=> Z Gate
qbec = H(3)*H(4)*CNOT(2, 0)*CNOT(3, 0)*CNOT(4, 0)*H(1)*H(4)*CNOT(2, 1)*\
        CNOT(4, 1)*H(2)*CNOT(3, 2)*CNOT(4, 2)*H(3)*H(4)*CNOT(4, 3)*Z(4)*H(4)*Z(4)
pprint(qbec)
alt_ec = CNOT(4, 0)*CNOT(4, 1)*CNOT(4, 2)*CNOT(4, 3)
