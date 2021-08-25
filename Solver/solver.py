from itertools import combinations
import xpress as xp

import numpy as np

from Solver.vars import Ivars
from typing import List, Set, Dict, Tuple, Optional

class Solver:

    def __init__(self, accs, vars: Dict[int, Ivars], i_mat, j_mat):
        self.accs = accs
        self.accsNum = len(accs)
        self.matches = np.array(list(combinations(self.accs, 2)))

        self.p = xp.problem()
        self.m = np.array([xp.var(vartype=xp.binary) for _ in self.matches])
        self.p.addVariable(self.m)

        self.vars = vars
        self.varsDict = {}

        self.Imat = i_mat
        self.Jmat = j_mat

        for period in vars.keys():
            if not vars[period].empty:
                self.varsDict[period] = np.array(
                    [[xp.var(vartype=xp.binary) for _ in vars[period].available] for _ in vars[period].inNeed])
                self.p.addVariable(self.varsDict[period])

    def set_constraints(self):
        # t is the index of the time period

        for acc in self.accs:
            acc_A_periods = np.nonzero(self.Imat[:, acc.index])
            for comb_acc in self.accs:
                acc_B_periods = np.nonzero(self.Jmat[:, comb_acc.index])
                filtered_periods = np.intersect1d(acc_A_periods, acc_B_periods)
                if filtered_periods.shape[0] > 0:
                    self.p.addConstraint(
                        xp.Sum(self.varsDict[t][self.Imat[t, acc.index]-1, self.Jmat[t, comb_acc.index]-1]
                               for t in filtered_periods)
                        <= self.m[self.get_match(acc, comb_acc)] * 1_000_000
                    )

            self.p.addConstraint(
                xp.Sum(self.m[k] for k in self.get_acc_matches(acc)) <= 1
            )

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
