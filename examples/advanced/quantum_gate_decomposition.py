"""
An example of decomposing multi-qubit gates into elementary gates is given.
"""

from sympy.physics.quantum.gate import CGate, Y, Z, SWAP
from sympy.printing.pretty import pprint
from sympy.physics.quantum.circuitplot import circuit_plot

print "Create some multi-qubit gates:"
print ""
# SWAP <=> Swap Gate
# Y <=> Y Gate
# Z <=> Z Gate
CY10 = CGate(1, Y(0))
print "Controlled-Y Gate"
pprint(CY10)
print ""
CZ01 = CGate(0, Z(1))
print "Controlled-Z Gate"
pprint(CZ01)
print ""
SWAP23 = SWAP(2, 3)
print "SWAP Gate"
pprint(SWAP23)
print ""

print "And now their decomposition:"
print ""
print "Decomposed controlled-Y Gate"
pprint(CY10.decompose())
circuit_plot(CY10.decompose(), nqubits=2)
print ""
print "Decomposed controlled-Z Gate"
pprint(CZ01.decompose())
circuit_plot(CZ01.decompose(), nqubits=2)
print ""
print "Decomposed SWAP Gate"
pprint(SWAP23.decompose())
circuit_plot(CY10.decompose(), nqubits=4)
