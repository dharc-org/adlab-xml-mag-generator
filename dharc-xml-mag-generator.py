#-*- coding: utf-8 -*-

# dharc-xml-mag-generator.py
# v0.4

import datetime
import exifread
import hashlib
import sys
import os

# get var from arguments
path = sys.argv[1]
ext = sys.argv[2]

# set vars
local = datetime.datetime.now()
creation = local.strftime("%Y-%m-%dT%H:%M:%S")

stprog = "http://example.stprog.org"
agency = "example agency"
title = "example title"

name= "TIFF"
mime = "image/tiff"

scanningagency = "example scanningagency"
devicesource = "example device"
scanner_manufacturer = "example manufacturer"
scanner_model = "example model"
capture_software = "example software"

# list all files with specific extension into "files" array
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if ext in file:
            files.append(os.path.join(r, file))
files.sort()

# xml mag header creation
xmlMagHeader = '''<?xml version="1.0" encoding="utf-8"?>
<mag:metadigit xmlns:mag="http://www.iccu.sbn.it/metaAG1.pdf"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:niso="http://www.niso.org/pdfs/DataDict.pdf" xmlns:xlink="http://www.w3.org/TR/xlink"
    version="2.0.1">
'''

xmlMagGen='''  <mag:gen creation="'''+creation+'''">
    <mag:stprog>'''+stprog+'''</mag:stprog>
    <mag:agency>'''+agency+'''</mag:agency>
    <mag:access_rights>1</mag:access_rights>
    <mag:completeness>0</mag:completeness>
  </mag:gen>
'''

xmlMagBib='''  <mag:bib level="m">
    <dc:identifier>'''+path+'''</dc:identifier>
    <dc:title>'''+title+'''</dc:title>
  </mag:bib>'''

xmlMagFooter='''</mag:metadigit>'''

print(xmlMagHeader+xmlMagGen+xmlMagBib)

# print arrays
i = 1
for f in files:
    # md5 sum
    md5 =  hashlib.md5(open(f, 'rb').read()).hexdigest()
    # filesize in Bytes
    filestats = os.stat(f)
    filesize = filestats.st_size
    # tags
    imgf = open(f, 'rb')
    tags = exifread.process_file(imgf)
    imagelength = tags['Image ImageLength']
    imagewidth = tags['Image ImageWidth']
    fileRes = tags['Image XResolution']
    # print mag:img with data
    print('''      <mag:img>
        <mag:sequence_number>'''+"{0:0=4d}".format(i)+'''</mag:sequence_number>
        <mag:nomenclature>PA</mag:nomenclature>
        <mag:usage>1</mag:usage>
        <mag:scale>0</mag:scale>
        <mag:file xlink:href="'''+f+'''" Location="URL" xlink:type="simple"/>
        <mag:md5>'''+md5+'''</mag:md5>
        <mag:filesize>'''+str(filesize)+'''</mag:filesize>
        <mag:image_dimensions>
          <niso:imagelength>'''+str(imagelength)+'''</niso:imagelength>
          <niso:imagewidth>'''+str(imagewidth)+'''</niso:imagewidth>
        </mag:image_dimensions>
        <mag:format>
          <niso:name>'''+name+'''</niso:name>
          <niso:mime>'''+mime+'''</niso:mime>
        </mag:format>
        <mag:scanning>
          <niso:scanningagency>'''+scanningagency+'''</niso:scanningagency>
          <niso:devicesource>'''+devicesource+'''</niso:devicesource>
          <niso:scanningsystem>
            <niso:scanner_manufacturer>'''+scanner_manufacturer+'''</niso:scanner_manufacturer>
            <niso:scanner_model>'''+scanner_model+'''</niso:scanner_model>
            <niso:capture_software>'''+capture_software+'''</niso:capture_software>
          </niso:scanningsystem>
        </mag:scanning>
      </mag:img>'''),
    i+=1

print(xmlMagFooter)
