# MusicXMLConverter

##Introduction

This tool is prepared for generating MusicXML scores from [SymbTr](https://github.com/MTG/SymbTr) txt files.

##Usage

```python
import os
from musicxmlconverter.symbtr2musicxml import symbtrscore

txtpath = 'path_to/kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi.txt'
mu2path = 'path_to/kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi.mu2'

symbtrname = kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi
mbid = {u'mbid': u'b43fd61e-522c-4af4-821d-db85722bf48c', u'type': u'work'}

outpath = out_path/kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi.xml

piece = symbtrscore(txtpath, mu2path, symbtrname=symbtrname, mbid=mbid) #txt info is fetched and attributes are calculated
xmlstr = piece.convertsymbtr2xml()  # outputs the xml score as string
piece.writexml(outpath)  # you can also save the score to a file after calling the conversion method above
```

##Installation

If you want to install musicxmlconverter, it is recommended to install musicxmlconverter and its dependencies into a virtualenv. In the terminal, do the following:
```
virtualenv env
source env/bin/activate
python setup.py install
```
If you want to be able to edit files and have the changes be reflected, then install musicxmlconverter like this instead
```
pip install -e .
```
Now you can install the rest of the dependencies:
```
pip install -r requirements
```
