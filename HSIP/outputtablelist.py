# coding: utf-8
import getpass
import os
import os.path as op
from bs4 import BeautifulSoup

SOURCEDIR = op.abspath(r"Output")
# DESTDIR = "/var/www/html/metadata/urbis/xml/hsip"
DEBUG=False

if __name__ == '__main__':

    outputset = [["Title", "table"]]


    for d in os.listdir(SOURCEDIR):
        sectionsourcefolder = op.join(SOURCEDIR, d)
        for f in os.listdir(sectionsourcefolder):
            if f.endswith('xml'):
                with open(op.join(SOURCEDIR, d, f), 'r') as fin:
                    soup = BeautifulSoup(fin.read(), "xml")
                    outputset.append([soup.findAll('title')[0].text, f.strip('.xml')])
    with open('tablereferences.csv', 'w') as fout:
        for z in outputset:
            fout.write(",".join(z) + '\n')

