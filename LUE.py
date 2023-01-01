import rasterio
import numpy as np
from xml.dom import minidom
from tkinter import filedialog
from tkinter import *
import os
import glob
import image

root = Tk()
root.filename = filedialog.askdirectory(initialdir="/", title="Pilih Folder")
map = root.filename
root.destroy()

gambar = glob.glob(os.path.join(map)+"\*.tif")

with rasterio.open(gambar[0]) as src:
    b4 = src.read(1)

with rasterio.open(gambar[1]) as src:
    b5 = src.read(1)

print("*"*30)
print("Have Done")
print("*"*30)
print("Go to the next!")

image.day_of_year()
image.data_LUE()

image.cal_sat(b4, b5, src)
image.b4_cal(src)
print("Perhitungan B4_Reflektans")
image.b5_cal(src)
print("Perhitungan B5_Reflektans")

gambar = glob.glob(os.path.join(map)+"\*reflectance.tif")

with rasterio.open(gambar[0]) as src:
    print("b4:", gambar[0])
    b4 = src.read(1)

with rasterio.open(gambar[1]) as src:
    print("b5:", gambar[1])
    b5 = src.read(1)
    
image.Hitung_NDVI(b4,b5,src)
print("Calculation of NDVI")
    
image.Hitung_SAVI(b4,b5,src)
print("Calculation of SAVI")

image.Hitung_LAI(src)
print("Calculation of LAI")

image.Hitung_FAPAR(src)
print("Calculation of FAPAR")

image.Hitung_GPP(src)
print("Calculation of GPP")

image.Hitung_Ra(src)
print("Calculation of Ra")

image.Hitung_NPP(src)
print("Calculation of NPP")

print("*"*30)
print("Well Done")
print("*"*30)