"""
An example of decomposing multi-qubit gates into elementary gates is given.
"""

from sympy.physics.quantum.gate import CGate, YGate, ZGate, SwapGate
from sympy.printing.pretty import pprint

print "Create some multi-qubit gates:"
print ""
CY10 = CGate(1, YGate(0))
print "Controlled-Y Gate"
pprint(CY10)
print ""
CZ01 = CGate(0, ZGate(1))
print "Controlled-Z Gate"
pprint(CZ01)
print ""
SWAP23 = SwapGate(2, 3)
print "SWAP Gate"
pprint(SWAP23)
print ""

print "And now their decomposition:"
print ""
print "Decomposed controlled-Y Gate"
pprint(CY10.decompose())
print ""
print "Decomposed controlled-Z Gate"
pprint(CZ01.decompose())
print ""
print "Decomposed SWAP Gate"
pprint(SWAP23.decompose())
