import os
from musicxmlconverter.symbtr2musicxml import SymbTrScore


def test_converter():
    # inputs
    scorename = 'kurdi--turku--sofyan--dalda_cikmis--'

    txtpath = os.path.join('sampledata', scorename + '.txt')
    mu2path = os.path.join('sampledata', scorename + '.mu2')
    xmlpath = os.path.join('sampledata', scorename + '.xml')

    mbid_url = 'http://musicbrainz.org/work/50bc4b54-5e14-4a98-bd44-ee5493479c7d'

    piece = SymbTrScore(txtpath, mu2path, symbtrname=scorename,
                        mbid_url=mbid_url)
    xmlstr = piece.convertsymbtr2xml()  # outputs the xml score as string

    with open(xmlpath, 'r') as savedxmlfile:
        savedxmlstr = savedxmlfile.read()

    assert savedxmlstr == xmlstr
