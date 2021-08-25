from itertools import combinations
import xpress as xp

import numpy as np


class Solver:

    def __init__(self, accs, intervals):
        self.accs = accs
        self.accsNum = len(accs)
        self.intervals = intervals
        self.intNum = len(intervals)
        self.matches = np.array(list(combinations(self.accs, 2)))

        self.p = xp.problem()
        self.x = np.array([[[xp.var(vartype=xp.binary) for _ in intervals] for _ in accs] for _ in self.accs])
        self.m = np.array([xp.var(vartype=xp.binary) for _ in self.matches])

        self.p.addVariable(self.x, self.m)

    def set_constraints(self):
        # t is the index of the time period

        for acc in self.accs:
            # no self colab
            for t in range(self.intNum):
                self.p.addConstraint(self.x[acc.index, acc.index, t] == 0)

            self.p.addConstraint(xp.Sum(self.m[k] for k in self.get_acc_matches(acc)) <= 1)

        # colab with only one for each interval
        for acc_A in self.accs:
            for t in range(self.intNum):
                self.p.addConstraint(
                    xp.Sum(self.x[acc_A.index, acc_B.index, t] for acc_B in self.accs) <= 1
                )

        k = 0
        for match in self.matches:
            acc_A, acc_B = match[0], match[1]
            self.p.addConstraint(
                xp.Sum(self.x[acc_A.index, acc_B.index, t] for t in range(self.intNum)) <= self.m[k]
            )
            k += 1

    def get_acc_matches(self, acc):
        indexes = []
        k = 0
        for match in self.matches:
            if acc.index == match[0].index or acc.index == match[1].index:
                indexes.append(k)
            k += 1

        return indexes
