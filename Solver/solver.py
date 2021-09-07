from itertools import combinations
import xpress as xp
from typing import List
from ACC.acc import Acc, DailyConfiguration

import numpy as np


class Solver:

    def __init__(self, accs: List[Acc], intervals):
        self.accs = accs
        self.accsNum = len(accs)
        self.intervals = intervals
        self.intervalsNum = len(intervals)
        self.matches = np.array(list(combinations(self.accs, 2)))

        self.p = xp.problem()
        self.d = np.array([[[xp.var(vartype=xp.integer) for _ in intervals] for _ in self.accs] for _ in self.accs])
        self.m = np.array([xp.var(vartype=xp.binary) for _ in self.matches])

        self.p.addVariable(self.d, self.m)

    def set_constraints(self):
        # t is the index of the time period

        for acc in self.accs:
            # no self colab
            for t in range(self.intervalsNum):
                # if acc.
                self.p.addConstraint(xp.Sum(self.d[acc.index, acc.index, t]) == 0)

            self.p.addConstraint(xp.Sum(self.m[k] for k in self.get_acc_matches(acc)) <= 1)

        # colab with only one for each interval
        for acc_A in self.accs:
            for t in range(self.intervalsNum):
                self.p.addConstraint(
                    xp.Sum(self.x[acc_A.index, acc_B.index, t] for acc_B in self.accs) <= 1
                )

        k = 0
        for match in self.matches:
            acc_A, acc_B = match[0], match[1]
            self.p.addConstraint(
                xp.Sum(self.x[acc_A.index, acc_B.index, t] for t in range(self.intervalsNum)) <= self.m[k]
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

    def get_match(self, acc_A, acc_B):
        k = 0
        for match in self.matches:
            if (acc_A.index == match[0].index and acc_B.index == match[1].index) or \
                    (acc_B.index == match[0].index and acc_A.index == match[1].index):
                return k

