from itertools import combinations

import numpy as np


class Solver:

    def __init__(self, accs):
        self.accs = accs
        self.matches = np.array(list(combinations(self.accs, 2)))
