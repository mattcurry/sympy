from sympy.physics.quantum.gate import X, Y, Z, H, S, T, CNOT, gate_simp
from sympy.physics.quantum.represent import represent

numqubits = 3

Xs = [X(i) for i in xrange(numqubits)]
Ys = [Y(i) for i in xrange(numqubits)]
Zs = [Z(i) for i in xrange(numqubits)]
Hs = [H(i) for i in xrange(numqubits)]
Ss = [S(i) for i in xrange(numqubits)]
Ts = [T(i) for i in xrange(numqubits)]
CNOTs = [CNOT(i,j) for i in xrange(numqubits) for j in xrange(numqubits) if i != j]

gate_list = Xs+Ys+Zs+Hs+Ss+Ts+CNOTs

base = len(gate_list)

xs = [represent(X(i), nqubits=numqubits) for i in xrange(numqubits)]
ys = [represent(Y(i), nqubits=numqubits) for i in xrange(numqubits)]
zs = [represent(Z(i), nqubits=numqubits) for i in xrange(numqubits)]
hs = [represent(H(i), nqubits=numqubits) for i in xrange(numqubits)]
ss = [represent(S(i), nqubits=numqubits) for i in xrange(numqubits)]
ts = [represent(T(i), nqubits=numqubits) for i in xrange(numqubits)]
cnots = [represent(CNOT(i,j), nqubits=numqubits) for i in xrange(numqubits) for j in xrange(numqubits) if i != j]

matrix_list = xs+ys+zs+hs+ss+ts+cnots

num = 0

# count(base, num)

def number_to_gates(number):
    gates = []
    for digit in number:
        gates.append(gate_list[digit])
    return gates

def number_to_matrices(number):
    matrices = []
    for digit in number:
        matrices.append(matrix_list[digit])
    return matrices

while True:
    gates = number_to_gates(num)
    if len(gate_simp(gates)) == base:
        
