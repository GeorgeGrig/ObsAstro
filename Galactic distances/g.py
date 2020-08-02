import math
import numpy as np
import pandas as pd
import csv

DATA = "tf.txt"
r_0 = 0.2
#Read data file
with open(DATA) as f:
    lines = f.readlines()
    f.close()
#For each line in the data file
csv_out = [["M_R", "X","r (Mpc)"]]
for line in lines:
    #data grooming
    line = line.strip()
    column = line.split()
    if column != [] and column[0] != "mR":
        m_r = float(column[0])
        ba = float(column[1])
        w_obs = float(column[2])
        X = m_r +8.09*(math.log10(w_obs)-2.5)
        i = math.acos(math.sqrt((ba**2-r_0**2)/(1-r_0**2)))
        w_real = w_obs/math.sin(i)
        Mr = -8.09*(math.log10(w_real) - 2.5) - 21.05
        r = 10**((m_r-Mr-25)/5)
        csv_out.append([Mr,X,r])

with open("out_e.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_out)