from itertools import combinations

import pandas as pd
import xpress as xp
from typing import List
from ACC.acc import Acc, DailyConfiguration

import numpy as np

xp.controls.outputlog = 0

intervals = [i for i in range(0, 1440, 60)]


class Solver1:

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
        self.x = np.array([[[[xp.var(vartype=xp.binary) for _ in intervals] for _ in days]
                            for _ in self.accs] for _ in self.accs])

        self.p.addVariable(self.d, self.x)

        self.initialDelay = sum(acc.totalDelay for acc in self.accs)
        self.reduction = None
        self.finalDelay = None
        self.services = 0

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
                    self.p.addConstraint(
                        self.x[acc.index, acc.index, day, t] == 0
                    )

                    self.p.addConstraint(
                        xp.Sum(self.x[acc.index, other.index, day, t] for other in self.accs) <= 1
                    )

                    self.p.addConstraint(
                        xp.Sum(self.x[other.index, acc.index, day, t] for other in self.accs) <= 1
                    )

        for acc_a in self.accs:
            for acc_b in self.accs:
                if acc_a.index != acc_b.index:
                    for day in range(self.numDays):
                        for t in range(self.intervalsNum):

                            if acc_a.days[day].inNeed[t]:
                                self.p.addConstraint(
                                    self.d[acc_a.index, acc_b.index, day, t] <= self.get_bound(acc_a, acc_b, day, t) *
                                    self.x[acc_a.index, acc_b.index, day, t]
                                )
                            else:

                                self.p.addConstraint(
                                    self.d[acc_a.index, acc_b.index, day, t] == 0
                                )
                                self.p.addConstraint(
                                    self.x[acc_a.index, acc_b.index, day, t] == 0
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

        self.delaySolution = self.p.getSolution(self.d)
        self.reduction = self.p.getObjVal()

        self.set_solution()

    @staticmethod
    def get_bound(acc_a: Acc, acc_b: Acc, day, t):
        acc_b_capacity = acc_b.days[day].spareCapacity[t] * acc_b.sector_capacity
        delayed_flights = acc_a.days[day].delayedFlights[t]

        return sum(delayed_flights[: min([len(delayed_flights), acc_b_capacity])])

    def set_solution(self):

        for acc_a in self.accs:
            for acc_b in self.accs:
                for d in range(self.numDays):
                    for t in range(self.intervalsNum):
                        if self.delaySolution[acc_a.index][acc_b.index][d][t] > 0.5:
                            acc_a.reduction += self.delaySolution[acc_a.index][acc_b.index][d][t]
                            acc_a.collaborations += 1
                            self.services += 1

            acc_a.newDelay = acc_a.totalDelay - acc_a.reduction

        self.finalDelay = self.initialDelay - self.reduction

    def make_df(self, name, tolerance, cap_correction, df_tot=None, save=False):
        columns = ["acc", "saturation tolerance", "capacity correction" + "initial delay", "final delay", "reduction"] \
                  + [acc.name for acc in self.accs] + ["case"]
        df = pd.DataFrame(columns=columns)
        total = ["total"] + [tolerance] + [cap_correction] + [self.initialDelay] + [self.finalDelay] \
                + [self.reduction] + ["" for _ in self.accs] + [name]
        df = df.append(dict(zip(columns, total)), ignore_index=True)

        for acc in self.accs:

            given = []

            for other_acc in self.accs:
                given.append(sum([self.delaySolution[acc.index, other_acc.index, d, t]
                                  for d in range(self.numDays) for t in range(self.intervalsNum)]))

            to_append = [acc.name] + [tolerance] + [cap_correction] + [acc.totalDelay] + [acc.newDelay] \
                        + [acc.reduction] + given + [name]

            df = df.append(dict(zip(columns, to_append)), ignore_index=True)

        if save:
            df.to_csv("Results/" + name + "_" + str(tolerance) + +str(cap_correction) + ".csv", index_label=False,
                      index=False)

        print(df)

        if df_tot is not None:
            df_tot = df_tot.append(df, ignore_index=True)
            return df_tot

        else:
            return df
