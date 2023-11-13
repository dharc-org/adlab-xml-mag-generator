# adlab-xml-mag-generator
Create xml with the mag format from a folder of image files

# dependency
Python ExifRead: https://pypi.org/project/ExifRead/
```sh
pip install exifread
```

# mag xml
Manual & info: https://www.iccu.sbn.it/export/sites/iccu/documenti/manuale.html

# example
The scripts need 3 arguments:
1) Custom config.json with personalized data
2) Folder with images
3) Extension of files
```sh
$ python adlab-xml-mag-generator.py config.json 1954/Q_1954_12 .tif
```
