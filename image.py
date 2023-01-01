import rasterio
import numpy as np
from tkinter import *
import MTL_Read_File as MTL
import datetime
import math

np.seterr(divide = 'ignore', invalid = 'ignore')

def day_of_year():
    global date , doy

    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Pilih FIle MTL",
                                               filetypes=(("LC08_L1TP_117060_20200403_20200410_01_T1_MTL", "*.txt"), 
                                                          ("All data", "*.*")))
    test = root.filename

    root.destroy()

    folder = MTL.Year()
    variable = folder.readFileLineByLine(test, 75)
    for i in variable:
        i = i.strip('\n')
        i = i.strip('\r')
        i = i.strip(' ')

    file = open(test)  
    #file.seek(774) for 2020
    file.seek(773)  #773 for 2015	
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    date = (file.read(10))
    format = "%Y-%m-%d"
    dt = datetime.datetime.strptime(date, format)
    tt = dt.timetuple()
    doy = float(tt.tm_yday)
    print("Day of Year =", doy)

def data_LUE():
    global PAR, GPP, LUE
    global PAR, GPP, LUE

    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Data LUE",
                                               filetypes=(("Data LUE", "*.txt"), ("All Data", "*.*")))

    setting = root.filename

    root.destroy()


    folder = MTL.Year()
    variable = folder.readFileLineByLine(setting, 0)
    for i in variable:
        i = i.strip('\n')
        i = i.strip('\r')
        i = i.strip(' ')

    PAR = float(variable[1].split("=")[1])
    GPP = float(variable[2].split("=")[1])
    LUE = float(variable[3].split("=")[1])
    
    print("PAR Daily", PAR)
    print("GPP Daily", GPP)
    print("GPP Daily", LUE)
   
def cal_sat(b4, b5, src):
    global b4_ref, b5_ref
    #metadata adjustment
    b4_ref = 0.0099809 * b4 - 49.90435
    b5_ref = 0.0061078 * b5 - 30.53898
    
def b4_cal(src):
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_b4_reflectance.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, b4_ref.astype(rasterio.float32))

def b5_cal(src):
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_b5_reflectance.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, b5_ref.astype(rasterio.float32))
 
def Hitung_NDVI(b4, b5, src):
    global NDVI
    NDVI = (b5.astype(float) - b4.astype(float)) / (b5.astype(float) + b4.astype(float))
    
    kwargs = src.meta
    kwargs.update(dtype = rasterio.float32, count = 1)
    with rasterio.open(str(date) + "_NDVI.tif" , "w", **kwargs) as dst:
        return dst.write_band(1, NDVI.astype(rasterio.float32))
 
    
def Hitung_SAVI(b4,b5,src):
    global SAVI
    SAVI = (1.1* (b5.astype(float) - b4.astype(float))) / (0.1+ b5.astype(float) + b4.astype(float))
    
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_SAVI.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, SAVI.astype(rasterio.float32))
    
def Hitung_LAI(src):
    global LAI
    LAI = np.where(SAVI < 0.817, np.power(SAVI, 3) * 11, 6)
    
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_LAI.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, LAI.astype(rasterio.float32))
    
def Hitung_FAPAR(src):
    global FAPAR
    FAPAR = 1 - np.exp(-0.47 * LAI) #7-12 y.o. (Landsat 8)
    
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_FAPAR.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, FAPAR.astype(rasterio.float32))
    
def Hitung_GPP(src):
    global GPP_1
    GPP_1 = LUE * FAPAR * PAR

    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_GPP.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, GPP_1.astype(rasterio.float32))

def Hitung_Ra(src):
    global Ra
    Ra = 0.45 * GPP_1
    
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_Ra.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, Ra.astype(rasterio.float32))
    
def Hitung_NPP(src):
    global NPP
    NPP = GPP_1 - Ra
    
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count=1)
    with rasterio.open(str((date))+'_NPP.tif', 'w', **kwargs) as dst:
        return dst.write_band(1, NPP.astype(rasterio.float32))
    
    