from sympy import Basic, Mul
from sympy.physics.quantum.gate import X, Y, Z, S, T, H, CNOT, SWAP

class GateRule(Basic):

    @property
    def lhs(self):
        return self.args

#    @property
#    def rhs(self):
#        return self.args[1]

    def match(self, e):
        # Go through and return an equivalent expression to e, or None
        # This uses self.lhs and self.rhs to find things == e
        rule = list(self.lhs[0].args)
        gate_num = len(rule)
        if isinstance(e, Mul):
            expr = list(e.args)
            rexpr = expr[:]
            expr.reverse()
            expr_len = len(expr)
        else:
            expr = [e]
            rexpr = [e]
            expr_len = 1
        if len(expr) > gate_num:
            return None
        else:
            return_rules = []
            for c in range(gate_num):
                rule.append(rule.pop(0))
                if rule[:expr_len] == expr:
                    if Mul(*rule[expr_len:]) not in return_rules:
                        return_rules.append(Mul(*rule[expr_len:]))
                if rule[-expr_len:] == expr:
                    if Mul(*rule[:-expr_len]) not in return_rules:
                        return_rules.append(Mul(*rule[:-expr_len]))
                if rule[:expr_len] == rexpr:
                    rrule = rule[expr_len:]
                    rrule.reverse()
                    if Mul(*rrule) not in return_rules:
                        return_rules.append(Mul(*rrule))
                if rule[-expr_len:] == rexpr:
                    rrule = rule[:-expr_len]
                    rrule.reverse()
                    if Mul(*rrule) not in return_rules:
                        return_rules.append(Mul(*rrule))
            return return_rules
        return None

_known_rules = []
_known_rules.append(GateRule(H(0)*X(0)*H(0)*Z(0)))
_known_rules.append(GateRule(CNOT(1,0)*X(1)*CNOT(1,0)*X(1)*X(0)))
_known_rules.append(GateRule(CNOT(1,0)*Y(1)*CNOT(1,0)*Y(1)*X(0)))
_known_rules.append(GateRule(CNOT(1,0)*Y(0)*CNOT(1,0)*Y(0)*Z(1)))
_known_rules.append(GateRule(CNOT(1,0)*Z(0)*CNOT(1,0)*Z(0)*Z(1)))
_known_rules.append(GateRule(CNOT(1,0)*H(0)*H(1)*CNOT(0,1)*H(1)*H(0)))
_known_rules.append(GateRule(CNOT(1,0)*Y(1)*Z(0)*CNOT(1,0)*X(1)*Y(0)))

def match_gate_rules(e):
    result = []
    for rule in _known_rules:
        r = rule.match(e)
        if r is not None:
            result.extend(r)
    return result
