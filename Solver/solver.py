from itertools import combinations
import xpress as xp
from typing import List
from ACC.acc import Acc, DailyConfiguration

import numpy as np

xp.controls.outputlog = 0

intervals = [i for i in range(0, 1440, 60)]


class Solver:

    def __init__(self, accs: List[Acc], days):
        self.accs = accs
        self.accsNum = len(accs)
        self.days = days
        self.numDays = len(self.days)
        self.intervals = intervals
        self.intervalsNum = len(intervals)
        self.matches = np.array(list(combinations(self.accs, 2)))

        self.p = xp.problem()
        self.d = np.array([[[[xp.var(vartype=xp.integer) for _ in intervals] for _ in days]
                            for _ in self.accs] for _ in self.accs])
        self.m = np.array([xp.var(vartype=xp.binary) for _ in self.matches])

        self.p.addVariable(self.d, self.m)

        self.combinationSolution = None
        self.delaySolution = None
        self.collaborations = None

    def set_constraints(self):
        # t is the index of the time period

        for acc in self.accs:
            for day in range(self.numDays):
                for t in range(self.intervalsNum):
                    # no self collaboration
                    self.p.addConstraint(
                        self.d[acc.index, acc.index, day, t] == 0
                    )
            # only one to one collaboration
            self.p.addConstraint(
                xp.Sum(self.m[index] for index in self.get_acc_matches(acc)) <= 1
            )

        for m in self.matches:
            acc_a, acc_b = m[0], m[1]
            # delay transfer only if collaborating
            self.p.addConstraint(
                xp.Sum(self.d[acc_a.index, acc_b.index, day, t]
                       for day in range(self.numDays) for t in range(self.intervalsNum)) <=
                self.m[self.get_match(acc_a, acc_b)] * 10_000_000
            )

        for acc_a in self.accs:
            for acc_b in self.accs:
                if acc_a.index != acc_b.index:
                    for day in range(self.numDays):
                        for t in range(self.intervalsNum):

                            if acc_a.days[day].inNeed[t]:
                                self.p.addConstraint(
                                    self.d[acc_a.index, acc_b.index, day, t] <= self.get_bound(acc_a, acc_b, day, t)
                                )
                            else:

                                self.p.addConstraint(
                                    self.d[acc_a.index, acc_b.index, day, t] == 0
                                )

    def set_objective(self):
        self.p.setObjective(xp.Sum(self.d[acc_a.index, acc_b.index, day, t]
                                   for acc_a in self.accs for acc_b in self.accs
                                   for day in range(self.numDays) for t in range(self.intervalsNum)),
                            sense=xp.maximize)

    def run(self):
        self.set_constraints()
        self.set_objective()
        self.p.solve()
        print(self.p.getProbStatusString())

        self.combinationSolution = self.p.getSolution(self.m)
        self.delaySolution = self.p.getSolution(self.d)

        self.collaborations = [self.matches[i] for i in range(len(self.matches))
                               if np.round(self.combinationSolution[i]) == 1]

    def report(self):
        print("total delay reduction:", self.p.getObjVal(), "minutes\n")
        print("optimal collaboration")
        for c in self.collaborations:
            print(c[0], c[1])

    def get_acc_matches(self, acc):
        indexes = []
        k = 0
        for match in self.matches:
            if acc.index == match[0].index or acc.index == match[1].index:
                indexes.append(k)
            k += 1

        return indexes

    def get_match(self, acc_a, acc_b):
        k = 0
        for match in self.matches:
            if (acc_a.index == match[0].index and acc_b.index == match[1].index) or \
                    (acc_b.index == match[0].index and acc_a.index == match[1].index):
                return k
            k += 1

    @staticmethod
    def get_bound(acc_a: Acc, acc_b: Acc, day, t):
        acc_b_capacity = acc_b.days[day].spareCapacity[t] * acc_b.sector_capacity
        delayed_flights = acc_a.days[day].delayedFlights[t]

        return sum(delayed_flights[: min([len(delayed_flights), acc_b_capacity])])
