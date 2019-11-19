#-*- coding: utf-8 -*-

# dharc-xml-mag-generator.py
# v0.4

import exifread
import hashlib
import sys
import os

# get var from arguments
path = sys.argv[1]
ext = sys.argv[2]

# set vars
scanningagency = "da definire"
devicesource = "Scanner"
scanner_manufacturer = "Plustek"
scanner_model = "OpticBook 4800"
capture_software = "da definire"

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

xmlMagGen='''  <mag:gen creation="2019-04-11T09:49:45">
    <mag:stprog>http://ficlit.unibo.it/</mag:stprog>
    <mag:agency>Dipartimento di Filologia Classica e Italianistica - FICLIT</mag:agency>
    <mag:access_rights>1</mag:access_rights>
    <mag:completeness>0</mag:completeness>
  </mag:gen>
'''

xmlMagBib='''  <mag:bib level="m">
    <dc:identifier>'''+path+'''</dc:identifier>
    <dc:title>Manoscritti arabi</dc:title>
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

#./prova/Q_3_1955_0001_piatto_ant.tif
#{'Image SubfileType': (0x00FE) Long=Full-resolution Image @ 26851518,
# 'Image ImageWidth': (0x0100) Short=2550 @ 26851530,
# 'Image ImageLength': (0x0101) Short=3510 @ 26851542,
# 'Image BitsPerSample': (0x0102) Short=[8, 8, 8] @ 26851682,
# 'Image Compression': (0x0103) Short=Uncompressed @ 26851566,
# 'Image PhotometricInterpretation': (0x0106) Short=2 @ 26851578,
# 'Image StripOffsets': (0x0111) Long=[] @ 26851688,
# 'Image SamplesPerPixel': (0x0115) Short=3 @ 26851602,
# 'Image RowsPerStrip': (0x0116) #Short=1 @ 26851614,
# 'Image StripByteCounts': (0x0117) Long=[] @ 26865728,
# 'Image XResolution': (0x011A) Ratio=300 @ 26879768,
# 'Image YResolution': (0x011B) Ratio=300 @ 26879776,
# 'Image PlanarConfiguration': (0x011C) Short=1 @ 26851662,
# 'Image ResolutionUnit': (0x0128) Short=Pixels/Inch @ 26851674}

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
          <niso:name>TIFF</niso:name>
          <niso:mime>image/tiff</niso:mime>
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
