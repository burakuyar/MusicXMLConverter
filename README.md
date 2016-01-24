# MusicXMLConverter

Tools to generate MusicXML scores from [SymbTr](https://github.com/MTG/SymbTr) txt and mu2 files.

##Usage

```python
import os
from musicxmlconverter.symbtr2musicxml import symbtrscore

txtpath = 'path_to_symbtr_txt_file'
mu2path = 'path_to_symbtr_mu2_file'

# the symbtr-name without the extension, can be omitted if the original filename is kept
symbtrname = 'kurdilihicazkar--sarki--agiraksak--ehl-i_askin--tatyos_efendi'

# the related musicbrainz mbid is supplied as a url
mbid_url = 'http://musicbrainz.org/work/b43fd61e-522c-4af4-821d-db85722bf48c' 

# output path
outpath = 'path_to_symbtr_musicxml_output_file'

piece = symbtrscore(txtpath, mu2path, symbtrname=symbtrname, mbid_url=mbid_url) #txt info is fetched and attributes are calculated
xmlstr = piece.convertsymbtr2xml()  # xml conversion; outputs the xml score as string
piece.writexml(outpath)  # you can also save the score to a file after calling the conversion method above
```

You can refer to [demo.ipynb](https://github.com/burakuyar/MusicXMLConverter/blob/master/demo.ipynb) for an interactive demo.

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

## Authors
Burak Uyar	burakuyar@gmail.com  
Sertan Şentürk		contact@sertansenturk.com
