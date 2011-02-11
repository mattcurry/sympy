"""
An example of creating a 5-qubit encoding circuit is given.
"""

from sympy.physics.quantum.gate import H, Z, CNotGate
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
# H <=> HadamardGate
# Z <=> ZGate
qbec = H(3)*H(4)*CNotGate(2, 0)*CNotGate(3, 0)*CNotGate(4, 0)*H(1)*H(4)*CNotGate(2, 1)*\
        CNotGate(4, 1)*H(2)*CNotGate(3, 2)*CNotGate(4, 2)*H(3)*H(4)*CNotGate(4, 3)*\
        Z(4)*H(4)*Z(4)
pprint(qbec)
alt_ec = CNotGate(4, 0)*CNotGate(4, 1)*CNotGate(4, 2)*CNotGate(4, 3)
