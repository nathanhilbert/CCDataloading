
# coding: utf-8

# Export Metadata to FDGC Standard using Arcpy
# -------------------
# 
#  - Find all GDBs in HSIP Gold folder in \\ontodar\urbis
#  - For each dataset export Metadata using the arcpy tool
#  - Keep file structure and write output xmls
#  
# **MUST BE RUN IN PYTHON 2.7 32-bit -- Background Processing 64 bit has issues with connecting to GDBs**

# In[2]:

import arcpy
from arcpy import env
import os.path as op
import os
OUTPUTDIR = os.path.abspath(r"Output")
print OUTPUTDIR
BASEGDBDIR = r"\\ontodar\URBIS\HSIP_GOLD_2015\Data\Infrastructure"

#set local variables
dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = dir + r"Metadata\Translator\ARCGIS2FGDC.xml"

# find all of the gdbs
for root, dirs, files in os.walk(BASEGDBDIR):
    for d in dirs:
        if d.endswith(".gdb"):
            gdboutputdir = op.join(OUTPUTDIR, d.split('.')[0])
            if not op.exists(gdboutputdir):
                os.mkdir(gdboutputdir)
            arcpy.env.workspace = op.join(root, d)
            print "Processing", op.join(root,d)
            for fds in arcpy.ListDatasets('','feature') + ['']:
                for fc in arcpy.ListFeatureClasses('','',fds):
                    print "."
                    if not op.exists(op.join(gdboutputdir, "{0}.xml".format(fc))):
                        print fc
                        print translator
                        print op.join(gdboutputdir, "{0}.xml".format(fc))
                        arcpy.ExportMetadata_conversion(fc, translator, op.join(gdboutputdir, "{0}.xml".format(fc)))




# In[ ]:



