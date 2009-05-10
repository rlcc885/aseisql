# HFacer.py - regenerate the Scintilla.h and SciLexer.h files from the Scintilla.iface interface 
# definition file.
# The header files are copied to a temporary file apart from the section between a //++Autogenerated
# comment and a //--Autogenerated comment which is generated by the printHFile and printLexHFile
# functions. After the temporary file is created, it is copied back to the original file name.

import string
import sys
import os
import Face

def Contains(s,sub):
	return string.find(s, sub) != -1

def printLexHFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["FeatureType"] in ["val"]:
			if Contains(name, "SCE_") or Contains(name, "SCLEX_"):
				out.write("#define " + name + " " + v["Value"] + "\n")

def printHFile(f,out):
	for name in f.order:
		v = f.features[name]
		if v["Category"] != "Deprecated":
			if v["FeatureType"] in ["fun", "get", "set"]:
				featureDefineName = "SCI_" + string.upper(name)
				out.write("#define " + featureDefineName + " " + v["Value"] + "\n")
			elif v["FeatureType"] in ["evt"]:
				featureDefineName = "SCN_" + string.upper(name)
				out.write("#define " + featureDefineName + " " + v["Value"] + "\n")
			elif v["FeatureType"] in ["val"]:
				if not (Contains(name, "SCE_") or Contains(name, "SCLEX_")):
					out.write("#define " + name + " " + v["Value"] + "\n")

def CopyWithInsertion(input, output, genfn, definition):
	copying = 1
	for line in input.readlines():
		if copying:
			output.write(line)
		if Contains(line, "//++Autogenerated"):
			copying = 0
			genfn(definition, output)
		if Contains(line, "//--Autogenerated"):
			copying = 1
			output.write(line)

def Regenerate(filename, genfn, definition):
	tempname = "HFacer.tmp"
	out = open(tempname,"w")
	hfile = open(filename)
	CopyWithInsertion(hfile, out, genfn, definition)
	out.close()
	hfile.close()
	os.unlink(filename)
	os.rename(tempname, filename)

f = Face.Face()
f.ReadFromFile("Scintilla.iface")
Regenerate("Scintilla.h", printHFile, f)
Regenerate("SciLexer.h", printLexHFile, f)
