import pandas as pd
import numpy as np
import xpress as xp
from itertools import combinations

xp.controls.outputlog = 0


class Area:
    def __init__(self, name, index, df):
        self.name = name
        self.index = index
        self.capacity = dict(zip(df.period, df.capacity))
        self.demand = dict(zip(df.period, df.demand))
        self.matches = []

    def __repr__(self):
        return self.name


class Model:
    def __init__(self, areas_list, periods):
        self._areasList = areas_list
        self._periods = periods
        self._matches = np.array(list(combinations(self._areasList, 2)))

        self.p = xp.problem()

        self.e = np.array([[xp.var(vartype=xp.integer) for _ in self._periods] for _ in areas_list])
        self.y = np.array(
            [[[xp.var(vartype=xp.integer) for _ in self._periods] for _ in areas_list] for _ in areas_list])
        self.m = np.array([xp.var(vartype=xp.binary) for _ in self._matches])
        self.p.addVariable(self.e, self.y, self.m)

        self.flow = None
        self.solutionMatches = None

    def set_constraints(self):
        for a in range(len(self._areasList)):
            for t in self._periods.keys():
                self.p.addConstraint(
                    self._areasList[a].demand[self._periods[t]]
                    - self._areasList[a].capacity[self._periods[t]]
                    - xp.Sum(
                        self.y[a, other_area, t] for other_area in range(len(self._areasList)))
                    + xp.Sum(
                        self.y[other_area, a, t] for other_area in range(len(self._areasList))) <=
                    self.e[a, t])

                available = 1 if (self._areasList[a].demand[self._periods[t]] - self._areasList[a].capacity[
                    self._periods[t]]) < 0 else 0

                self.p.addConstraint(xp.Sum(self.y[j, a, t] for j in range(len(self._areasList))) <= 10000 * available)

                self.p.addConstraint(
                    xp.Sum(self.y[a, j, t] for j in range(len(self._areasList))) <= 10000 * (1 - available))

            idxs = [i for i in range(len(self._matches)) if
                    self._matches[i][0].name == self._areasList[a].name or self._matches[i][1].name == self._areasList[
                        a].name]

            self.p.addConstraint(xp.Sum(self.m[i] for i in idxs) <= 1)

        for i in range(len(self._matches)):
            a = self._matches[i][0].index
            b = self._matches[i][1].index

            self.p.addConstraint(
                xp.Sum(self.y[a, b, t] + self.y[b, a, t] for t in self._periods.keys()) <= 10000 * self.m[i])

    def set_objective(self):
        self.p.setObjective(
            xp.Sum(xp.Sum(self.e[a, t] for t in self._periods.keys()) for a in range(len(self._areasList)))
            + 0.001 * xp.Sum(
                xp.Sum(xp.Sum(self.y[a, b, t] for t in self._periods.keys()) for a in range(len(self._areasList)))
                for b in range(len(self._areasList))), sense=xp.minimize)

    def run(self):
        self.set_constraints()
        self.set_objective()
        self.p.solve()

        self.flow = self.p.getSolution(self.y)

        initial = sum(
            [a.demand[t] - a.capacity[t] if a.demand[t] - a.capacity[t] > 0 else 0 for a in self._areasList
             for t in self._periods.values()])
        print("initial: ", initial, "   final: ", int(self.p.getObjVal()))

        self.solutionMatches = self.p.getSolution(self.m)
        for i in range(len(self.solutionMatches)):
            if self.solutionMatches[i] > 0.9:
                print(self._matches[i][0].name+" - "+self._matches[i][1].name)
                # for j in self._periods.keys():
                #     if self.flow[self._matches[i][0].index, self._matches[i][1].index, j] \
                #             + self.flow[self._matches[i][1].index, self._matches[i][0].index, j] >= 1:
                #
                #         print(int(self.flow[self._matches[i][0].index, self._matches[i][1].index, j]),
                #               int(self.flow[self._matches[i][1].index, self._matches[i][0].index, j]), "period:",j)
                #         print(int(
                #             self._matches[i][0].demand[self._periods[j]] -
                #             self._matches[i][0].capacity[self._periods[j]]),
                #               int(self._matches[i][1].demand[self._periods[j]] - self._matches[i][1].capacity[
                #                   self._periods[j]]))
                # print()
