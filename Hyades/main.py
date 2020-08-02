import math
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import pandas as pd

#Initial variables
DATA = "hyades_data.dat"
delta_cent = math.radians(5.8)    #in degrees
alpha_cent = math.radians(96.6)   #in degrees
r_cent = 46.34                    #in parsecs

def coords(r_a, dec):
    tot = str(r_a + " " + dec)
    c = SkyCoord(tot, unit=(u.hourangle, u.deg))
    tot = c.to_string('decimal').split()
    r_a = tot[0]
    dec = tot[1]
    return float(r_a),float(dec)

def theta_calc(al_st,d_st):
    al_st = math.radians(al_st)
    d_st = math.radians(d_st)
    return math.acos(math.sin(d_st)*math.sin(delta_cent)+ math.cos(d_st)*math.cos(delta_cent)*math.cos(al_st - alpha_cent))

def mvmnt_cal(macos,err_ma,m_delt,err_md):
    err_ma = err_ma/10**3
    err_md = err_md/10**3
    m = math.sqrt((macos/10**3)**2 + (m_delt/10**3)**2)
    err = math.sqrt((((macos/10**3)**2/m)**2)*err_ma**2 + (((m_delt/10**3)**2/m)**2)*err_md**2)
    return m, err

def dist_cntr(v_r,err_cntr,theta,m,err_m):
    v = v_r*math.tan(theta)
    r = v/(4.74*m)
    err_v = math.tan(theta)*err_cntr
    err_r = math.sqrt(((1/(4.74*m))**2)*err_v**2 + ((v/(4.74*m**2))**2)*err_m**2)
    return r, err_r, v, err_v

def dist_parallax(p,err_par):
    r = 10**3/p
    err = (10**3/p**2)*err_par
    return r, err

def data_parser():
    outputs = [['Name','Theta','υ','μ','r_p','r_μ','r_μ - r_π']]
    r_tot = 0
    r_err_tot = 0
    r_p_tot = 0
    r_p_err_tot = 0
    i = 0
    #Read data file
    with open(DATA) as f:
        lines = f.readlines()
        f.close()
    #For each line in the data file
    for line in lines:
        #data grooming
        line = line.strip()
        column = line.split()
        if column != []:#Ignores empty lines
            if "Name" not in column:#Ignores first line
                temp = []
                #Calculate right ascention and declination in degrees and store them to the correct posititon
                r_a = column[7] + " " + column[8] + " " + column[9]
                dec = column[10] + " " + column[11] + " " + column[12]
                r_a,dec = coords(r_a,dec)
                #Change datatype to float for calculations
                column=np.array(column,float)
                #Calculate theta
                theta = theta_calc(r_a,dec)
                #Calculate μ and errors
                m, m_err = mvmnt_cal(column[13],column[14],column[15],column[16])   
                #Calculate distance and errors
                r, r_err, v, v_err = dist_cntr(column[3],column[4],theta,m,m_err)
                print(r_err)
                _r = r
                if abs(r-r_cent)>10:
                    name = "*"+str(int(column[0]))+"*"
                else:
                    i += 1
                    name = str(int(column[0]))
                    r_tot += r #Need to calculate averages
                    r_err_tot += r_err**2 #Need to calculate averages
                #Calculate parallax distance and errors
                r_p, r_p_err = dist_parallax(column[1],column[2])
                _r_p = r_p
                if abs(r_p - r_cent) <= 10:
                    r_p_tot += r_p #Need to calculate averages
                    r_p_err_tot += r_p_err**2 #Need to calculate averages
                #Calculate dif between the two methods and the error
                r_dif = _r - _r_p
                r_dif_err = math.sqrt(r_err**2 + r_p_err**2)
                ##Populate output##
                temp.append(name)
                temp.append(round(theta,4))
                temp.append(str(round(v,4))+'±'+str(round(v_err,4)))
                temp.append(str(round(m,4))+'±'+str(round(m_err,8)))
                temp.append(str(round(r_p,4))+'±'+str(round(r_p_err,4)))
                temp.append(str(round(r,4))+'±'+str(round(r_err,4)))
                temp.append(str(round(r_dif,4))+'±'+str(round(r_dif_err,4)))
                outputs.append(temp)
    median_r = r_tot/(i)
    median_r_p = r_p_tot/(i)
    median_r_err = math.sqrt(r_err_tot)/(i)
    median_r_p_err = math.sqrt(r_p_err_tot)/(i)
    outputs.append(['Median r',(str(round(median_r,4))+'±'+str(round(median_r_err,6))), 'Median r parallax', (str(round(median_r_p,4))+'±'+str(round(median_r_p_err,4)))])
    df = pd.DataFrame.from_records(outputs)
    df.to_csv('temp.csv')
data_parser()