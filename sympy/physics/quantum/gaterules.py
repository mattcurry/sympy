from sympy import Basic
from sympy.physics.quantum.gate import X, Y, Z, S, T, H, CNOT, SWAP

class GateRule(Basic):

    @property
    def lhs(self):
        return self.args[0]

    @property
    def rhs(self):
        return self.args[1]

   def match(self, e):
        # Go through and return an equivalent expression to e, or None
        # This uses self.lhs and self.rhs to find things == e
        

_known_rules = []
_known_rules.append(GateRule(Z(0), H(0)*X(0)*H(0)))
_known_rules.append(GateRule(...))
_known_rules.append(GateRule(...))
_known_rules.append(GateRule(...))
_known_rules.append(GateRule(...))

def match_gate_rules(e):
    result = []
    for rule in _known_rules:
        r = rule.match(e)
        if r is not None:
            result.append(r)
    return result
