from sympy import Mul
from sympy.matrices import Matrix, eye
from sympy.physics.quantum.gate import X, Y, Z, H, S, T, CNOT, gate_simp
from sympy.physics.quantum.represent import represent

numqubits = 2

Xs = [X(i) for i in xrange(numqubits)]
Ys = [Y(i) for i in xrange(numqubits)]
Zs = [Z(i) for i in xrange(numqubits)]
Hs = [H(i) for i in xrange(numqubits)]
Ss = [S(i) for i in xrange(numqubits)]
Ts = [T(i) for i in xrange(numqubits)]
CNOTs = [CNOT(i,j) for i in xrange(numqubits) for j in xrange(numqubits) if i != j]

gate_list = Xs+Ys+Zs+Hs+Ss+Ts+CNOTs

base = len(gate_list)

xs = [represent(X(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
ys = [represent(Y(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
zs = [represent(Z(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
hs = [represent(H(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
ss = [represent(S(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
ts = [represent(T(i), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits)]
cnots = [represent(CNOT(i,j), nqubits=numqubits, format='scipy.sparse') for i in xrange(numqubits) for j in xrange(numqubits) if i != j]

matrix_list = xs+ys+zs+hs+ss+ts+cnots

num = [0,1]


def count(base, number):
    for i in xrange(len(number)):
        if number[i] == (base-1):
            number[i] = 0
        else:
            number[i] += 1
            break
    if number[i] == 0:
        number.append(1)

def number_to_gates(number):
    gates = []
    for digit in number:
        gates.append(gate_list[digit])
    return gates

def number_to_matrices(number):
    matrices = []
    if isinstance(number, int):
        return matrix_list[number]
    for digit in number:
        matrices.append(matrix_list[digit])
    return matrices

def matrix_mul(matrices):
    mul = eye(2**numqubits)
    for matrix in matrices:
        mul = mul*matrix
    return mul

def is_scalar_matrix(matrix):
    if list(matrix.nonzero()[0]) == list(matrix.nonzero()[1]):
        diag = list(matrix.diagonal())
        if diag.count(diag[0]) == len(diag):
            return True
    return False

while True:
    if num[0] is 0:
        matrices = number_to_matrices(num[1:])
        cached = matrix_mul(matrices)
    gates = number_to_gates(num)
    if len(gate_simp(Mul(*gates)).args) == len(gates):
        circuit = number_to_matrices(num[0])*cached
        if is_scalar_matrix(circuit):
            identities = open('/home/matt/Documents/gate_identities/%s-qubit_identities.txt' % numqubits, 'a')
            identities.write(str(gate_simp(Mul(*gates)).args)+'\n')
            identities.close()
            print num
            print gate_simp(Mul(*gates)).args
            print circuit
            print ''
    count(base, num)
