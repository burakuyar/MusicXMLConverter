# MusicXMLConverter

Tools to generate MusicXML scores from [SymbTr](https://github.com/MTG/SymbTr) txt and mu2 files.

## Usage

```python
from musicxmlconverter.symbtr2musicxml import SymbTrScore

txtpath = 'path_to_symbtr_txt_file'
mu2path = 'path_to_symbtr_mu2_file'

# the symbtr-name without the extension, can be omitted if the original
# filename is kept
symbtrname = 'kurdi--turku--sofyan--dalda_cikmis--'

# the related musicbrainz mbid is supplied as a url
mbid_url = 'http://musicbrainz.org/work/50bc4b54-5e14-4a98-bd44-ee5493479c7d'

# output path
outpath = 'path_to_symbtr_musicxml_output_file'

# instantiate the score object
piece = SymbTrScore(txtpath, mu2path, symbtrname=symbtrname, mbid_url=mbid_url)

# xml conversion; outputs the xml score as string
xmlstr = piece.convertsymbtr2xml()

# you can also save the score to a file after conversion
piece.writexml(outpath)
```

You can refer to [demo.ipynb](https://github.com/burakuyar/MusicXMLConverter/blob/master/demo.ipynb) for an interactive demo.

## Installation

If you want to install musicxmlconverter, it is recommended to install musicxmlconverter and its dependencies into a virtualenv. In the terminal, do the following:
```
virtualenv env
source env/bin/activate
python setup.py install
```
If you want to be able to edit files and have the changes be reflected, then install musicxmlconverter like this instead:
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
