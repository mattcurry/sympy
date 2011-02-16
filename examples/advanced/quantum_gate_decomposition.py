"""
An example of decomposing multi-qubit gates into elementary gates is given.
"""

from sympy.physics.quantum.gate import CGate, Y, Z, SWAP
from sympy.printing.pretty import pprint
from sympy.physics.quantum.circuitplot import circuit_plot

# SWAP <=> Swap Gate
# Y <=> Y Gate
# Z <=> Z Gate
CY10 = CGate(1, Y(0)); CY10
CZ01 = CGate(0, Z(1)); CZ01
SWAP10 = SWAP(1, 0); SWAP10

CY10.decompose()
circuit_plot(CY10.decompose(), nqubits=2)

CZ01.decompose()
circuit_plot(CZ01.decompose(), nqubits=2)

SWAP10.decompose()
circuit_plot(SWAP10.decompose(), nqubits=2)
