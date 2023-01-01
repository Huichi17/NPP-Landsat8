import zipfile, os
import string
import time 
from fnmatch import fnmatch
import shutil, sys

class Year(object):
	def browseFolder(self,root,pattern):
		
		lista = []
		#pattern = "*.lyr"
		for path, subdirs, files in os.walk(root):
			for name in files:
				if fnmatch(name.lower(), pattern):
					lista.append( os.path.join(path, name))
		return lista
	#filename of destination file
	#append = 0/1 
	#data = data tp write
	def WriteToFile(self,filename,append,data):	
		if(append==1):
			outfile = open(filename,'a')
			outfile.write( data)
			outfile.close()	
		else:
			outfile = open(filename,'w')
			outfile.write( data)
			outfile.close()	
	#path = file name
	#header = 0 is there is no line to skip from begining
	def readFileLineByLine(self,path, header):
		infile = open(path,'r')
		print ("file opened")
		data =[]
		counter1=0
		for line in infile:
			if counter1 < header:
				counter1=counter1+1
				continue			
			line = line.replace("\n",' ');				
			data.append(line)					
			counter1=counter1+1
		infile.close()	
		return data
