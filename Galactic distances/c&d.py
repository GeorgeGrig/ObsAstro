import math
import json
import csv

c = 299792.458
H = 70
def z(l_obs,l_lab):
    return float((l_obs-l_lab)/l_lab)

def r(_z):
    return c*_z/H

def coord_chng(l,b,v_0):
    v_LSR = v_0 +9*math.cos(l)*math.cos(b)+12*math.sin(l)*math.cos(b)+7*math.sin(b)
    v_G = v_LSR + 220*math.sin(l)*math.cos(b)
    v_LG = v_G - 62*math.cos(l)*math.cos(b)+40*math.sin(l)*math.cos(b)-35*math.sin(b)
    return v_LG

with open('./lines.json') as json_file:
    data = json.load(json_file)


csv_out = [["Name", "z", "r","z_corr", "r_corr"]]
for observation in data["Measured"]:
    for key in observation.keys():
        if key == "Name":
            i = 0
            _z = 0
        elif key == "Bands":
            for _key in observation[key].keys():
                _z = z(observation[key][_key],data["Emmited"][_key])
                i += 1
                _z += _z
        elif key == "Cords":
            l = observation[key]["RA"]
            b = observation[key]["DEC"]
            v_0 = c*_z/i
            v_LG = coord_chng(l,b,v_0)
            z_corr = v_LG/c
    csv_out.append([observation["Name"],_z/i,r(_z/i),z_corr,r(z_corr)])

with open("out_c_d.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_out)