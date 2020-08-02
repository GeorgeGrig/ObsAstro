#IMPORTS
import os
from PIL import Image, ImageOps
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import os.path
from os import path
#IMPORTS

#Functions
def get_concat_h(im1, im2):
    #This function concatinates the two images side by side
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def img_download(Year_start,Cur_Date,Month_start,size,filename,toggle):
    if toggle:
        urllib.request.urlretrieve(f"https://spaceweather.com/images{str(Year_start)}/0{str(Cur_Date)}{Month_start.lower()}{str(Year_start)[-2:]}/hmi1898.gif", "./Temp/"+f"{filename}_downloaded.png")
    else:
        urllib.request.urlretrieve(f"https://spaceweather.com/images{str(Year_start)}/{str(Cur_Date)}{Month_start.lower()}{str(Year_start)[-2:]}/hmi1898.gif", "./Temp/"+f"{filename}_downloaded.png")
    downloaded = Image.open("./Temp/"+f"{filename}_downloaded.png")
    downloaded = downloaded.resize(size)
    return ImageOps.mirror(downloaded)    

def list_populator(Month_start,Cur_Date,string,p_axis,hel_lat,toggle):
    if toggle:
        test_line = string.split(Month_start+" 0"+str(Cur_Date))[1]
        test_line = Month_start+" 0"+str(Cur_Date)+test_line
    else:
        test_line = string.split(Month_start+" "+str(Cur_Date))[1]
        test_line = Month_start+" "+str(Cur_Date)+test_line
    test_line = test_line.split("\n")[0]
    p_axis.append(str(test_line.split(" ")[-1]))
    hel_lat.append(str(test_line.split(" ")[-3]))
    return p_axis,hel_lat

def data_fetcher(Year_start,Cur_Date,Month_start,filename,toggle,retried):
    if not path.exists("./Temp/"+f"{filename}_downloaded.txt") or retried:
        if toggle:
            urllib.request.urlretrieve(f"https://spaceweather.com/images{str(Year_start)}/0{str(Cur_Date)}{Month_start.lower()}{str(Year_start)[-2:]}/sunspot_labels.txt", "./Temp/"+f"{filename}_downloaded.txt")
        else:
            urllib.request.urlretrieve(f"https://spaceweather.com/images{str(Year_start)}/{str(Cur_Date)}{Month_start.lower()}{str(Year_start)[-2:]}/sunspot_labels.txt", "./Temp/"+f"{filename}_downloaded.txt")
    f=open("./Temp/"+f"{filename}_downloaded.txt", "r")
    content = f.readlines()
    f.close
    sun_spots = []
    tot_cords = []
    g = 0
    f = 0
    labels = ("Name","Spot_lat","Spot_long","Spot_size","Num_spots","Type")
    if not content:
        table, yeet1, yeet2 = data_fetcher(Year_start,Cur_Date-1,Month_start,filename,toggle,True)
        print (f"text file {filename} was empty, will use previous day data")
    else:
        for line in content:
            entry = []
            name = line[:4]
            cords = line[5:11]
            spot_long = cords[3:6]
            spot_lat = cords[0:3]
            if "E" in spot_long:
                spot_long = -int(cords[4:6])
            else:
                spot_long = int(cords[4:6])
            if "S" in spot_lat:
                spot_lat = -int(cords[1:3])
            else:
                spot_lat = int(cords[1:3])
            spot_size = int(line[19:23])*0.2
            num_spots = round(int(line[34:36]) - int(line[34:36])*0.22)
            type = line[37:]
            if "-" in type:
                type = type.split("-")[1]
            type = type[0:1]
            if (num_spots <= 1) or (int(spot_size) <= 1 ) or (abs(int(spot_long)) >= 70) or type == "A": pass 
            else: 
                g += 1
                entry.append(name)  
                entry.append(spot_lat)   
                entry.append(spot_long)
                entry.append(spot_size) 
                entry.append(num_spots)
                entry.append(type)    
                tot_cords.append(spot_lat)  
                f += num_spots
                sun_spots.append(entry)
        #return sun_spots
        sun_spots.append(("","","","","",""))
        calcs = ("Visible groups",g,"f",f,"Wolf Number",10*g + f)
        sun_spots.append(calcs)
        plt.clf()
        plt.table(cellText=sun_spots,colLabels=labels,cellLoc = "center",loc="center")
        plt.subplots_adjust(left=0.125,right = 0.9 ,bottom = 0.1 ,top=0.9)
        plt.axis('off')
        #plt.axis('tight')
        plt.savefig("./Temp/"+f"{filename}_table.png")
        table_pic = Image.open("./Temp/"+f"{filename}_table.png").convert("RGBA")
        w, h = table_pic.size
        correction = len(content)*3.5
        table = table_pic.crop((76, 172-correction, w-60 , h-175+correction))
        w, h = table.size
        table = table.resize((1996,h*4))
    return table, 10*g + f, tot_cords

def DateExtractor():
    months = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
    filename = os.listdir("./Source")[0]
    Year_start = "20"+ filename[1:3]
    Month_start = months[int(filename[3:5])-1]
    return Year_start, Month_start

##Main function##
def main_thing():
    #Pre-Game#
    Year_start, Month_start = DateExtractor()
    f=open(f"./{Year_start}.html", "r")
    string = f.read()
    source_dir = "./Source"
    wolf_dir = "./WolfDiagrams"
    i = 0
    size = (998,998) 
    p_axis = []
    hel_lat = []   
    wolf_numbers = []
    Spots_cords = []
    days = []
    #Pre-Game#
    #Do for each jpg in source_dir:
    for file in os.listdir(source_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"): 
            image  = Image.open(os.path.join(source_dir, filename)).convert("RGBA")
            filename = filename.strip(".jpg")
            Cur_Date = int(filename[-2:])
            days.append(Cur_Date)
            if Cur_Date < 10:
                #Populate p axis and hel lat lists with the corresponding values
                p_axis,hel_lat = list_populator(Month_start,Cur_Date,string,p_axis,hel_lat,1)
                #Download corresponding image resize and mirror it
                downloaded = img_download(Year_start,Cur_Date,Month_start,size,filename,1)
                #Fetch data of the spots and add them to a table
                table, wolf_number,cords = data_fetcher(Year_start,Cur_Date,Month_start,filename,1,False)
                wolf_numbers.append(wolf_number)
                Spots_cords.append(cords)
            else:
                #Populate p axis and hel lat lists with the corresponding values
                p_axis,hel_lat = list_populator(Month_start,Cur_Date,string,p_axis,hel_lat,0)
                #Download corresponding image resize and mirror it
                downloaded = img_download(Year_start,Cur_Date,Month_start,size,filename,0)
                table, wolf_number, cords = data_fetcher(Year_start,Cur_Date,Month_start,filename,0,False)
                wolf_numbers.append(wolf_number)
                Spots_cords.append(cords)
            #Get wolf diagram overlay
            wolf_value = int(round(float(hel_lat[i])))
            if wolf_value < 0:
                wolf_value = abs(wolf_value)
                wolf = Image.open(os.path.join(wolf_dir, f"B{wolf_value}.jpg")).convert("RGBA")
                wolf = wolf.resize(size)
                wolf = wolf.rotate(180)
            else:
                wolf = Image.open(os.path.join(wolf_dir, f"B{wolf_value}.jpg")).convert("RGBA")
                wolf = wolf.resize(size)
            #Rotate source image to correct p_axis and superimpose wolf diagram overlay
            rotated = image.rotate(float(p_axis[i]))
            mask = Image.new("L", image.size, 128)
            new_img = Image.composite(rotated, wolf, mask)
            #Concatinate side by side the downloaded image with the processed one
            dst = get_concat_h(new_img, downloaded)
            dst = get_concat_v(dst, table)
            dst.save("./Output/"+f"{filename}.png")
            i += 1
            print("Done " + str(i))
            continue
        else:
            continue
    f.close
    plt.clf()
    plt.plot(days,wolf_numbers)
    plt.savefig("./Output/"+f"WolfNum_VS_Days.png")
    plt.clf()
    for xe, ye in zip(days, Spots_cords):
        plt.scatter([xe] * len(ye), ye)
    plt.xticks(days)
    plt.axes().set_xticklabels(['Days'])
    plt.axhline(y=0)
    plt.savefig("./Output/"+f"Butterfly_Diagram.png")
main_thing()