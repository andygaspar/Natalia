import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from datetime import timedelta
plt.rcParams["figure.figsize"] = (20,15)


df_saturation = pd.read_csv("data/ACCs_ActualCapacities/Saturation_1908.csv", sep= ";")

df_saturation.columns