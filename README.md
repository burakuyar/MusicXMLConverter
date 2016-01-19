# MusicXMLConverter

##Introduction

This tool is prepared for generating MusicXML scores from [SymbTr](https://github.com/MTG/SymbTr) txt files.

##Usage

```python
import os
from musicxmlconverter.symbtr2musicxml import symbtrscore

txtpath = SymbTr_txt_filename
mu2path = SymbTr_mu2_filename

symbtrname = 'kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi'
mbid = {u'mbid': u'b43fd61e-522c-4af4-821d-db85722bf48c', u'type': u'work'}

outpath = path_for_MusicXML_output

piece = symbtrscore(txtpath, mu2path, symbtrname=symbtrname, mbid=mbid) #txt info is fetched and attributes are calculated
xmlstr = piece.convertsymbtr2xml()  # outputs the xml score as string
piece.writexml(outpath)  # you can also save the score to a file after calling the conversion method above
```

