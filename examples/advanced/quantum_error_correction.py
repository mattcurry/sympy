"""
An example of 5-qubit error correcting code is given.

* Create codeword operators.
* Apply these operators to states.
* Plot encoding circuit.
"""

from sympy.physics.quantum.gate import H, X, Z, CNOT
from sympy.physics.quantum.qubit import IntQubit
from sympy.physics.quantum.applyops import apply_operators
from sympy.printing.pretty import pprint
from sympy.physics.quantum.circuitplot import circuit_plot
from sympy.core.numbers import Rational

M0 = Z(1)*X(2)*X(3)*Z(4); M0
M1 = Z(2)*X(3)*X(4)*Z(0); M1
M2 = Z(3)*X(4)*X(0)*Z(1); M2
M3 = Z(4)*X(0)*X(1)*Z(2); M3

zero = Rational(1,4)*(1+M0)*(1+M1)*(1+M2)*(1+M3)*IntQubit(0, 5); zero
apply_operators(zero)
one = Rational(1,4)*(1+M0)*(1+M1)*(1+M2)*(1+M3)*IntQubit(2**5-1, 5); one
apply_operators(one)

# CNOT <=> Controlled-Not Gate
# H <=> Hadamard Gate
# Z <=> Z Gate
encoding_circuit = H(3)*H(4)*CNOT(2, 0)*CNOT(3, 0)*CNOT(4, 0)*H(1)*H(4)*CNOT(2, 1)*\
        CNOT(4, 1)*H(2)*CNOT(3, 2)*CNOT(4, 2)*H(3)*H(4)*CNOT(4, 3)*Z(4)*H(4)*Z(4)
circuit_plot(encoding_circuit, nqubits=5)
