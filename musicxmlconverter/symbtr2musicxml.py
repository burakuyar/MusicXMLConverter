# -*- coding: utf-8 -*-
import numpy
import matplotlib.pyplot as plt
import os
import fnmatch
import copy
import symbtrnote
import getopt
import sys
import urllib
from types import *
from lxml import etree
import json
from symbtrdataextractor import extractor
from symbtrdataextractor import symbtrreader

# koma definitions
# flats
b_koma = 'quarter-flat'  # 'flat-down'
b_bakiyye = 'slash-flat'
b_kmucennep = 'flat'
b_bmucennep = 'double-slash-flat'

# sharps
d_koma = 'quarter-sharp'  # quarter-sharp    SWAP 1ST AND 3RD SHARPS
d_bakiyye = 'sharp'
d_kmucennep = 'slash-quarter-sharp'  # slash-quarter-sharp
d_bmucennep = 'slash-sharp'

# section list
sectionList = [u"1. HANE", u"2. HANE", u"3. HANE", u"4. HANE", u"TESLİM", u"TESLİM ", u"MÜLÂZİME", u"SERHÂNE",
               u"HÂNE-İ SÂNİ", u"HÂNE-İ SÂLİS", u"SERHANE", u"ORTA HANE", u"SON HANE", u"1. HANEYE", u"2. HANEYE",
               u"3. HANEYE", u"4. HANEYE", u"KARAR", u"1. HANE VE MÜLÂZİME", u"2. HANE VE MÜLÂZİME",
               u"3. HANE VE MÜLÂZİME", u"4. HANE VE MÜLÂZİME", u"1. HANE VE TESLİM", u"2. HANE VE TESLİM",
               u"3. HANE VE TESLİM", u"4. HANE VE TESLİM", u"ARANAĞME", u"ZEMİN", u"NAKARAT", u"MEYAN",
               u"SESLERLE NİNNİ", u"OYUN KISMI", u"ZEYBEK KISMI", u"GİRİŞ SAZI", u"GİRİŞ VE ARA SAZI", u"GİRİŞ",
               u"FİNAL", u"SAZ", u"ARA SAZI", u"SUSTA", u"KODA", u"DAVUL", u"RİTM", u"BANDO", u"MÜZİK", u"SERBEST",
               u"ARA TAKSİM", u"GEÇİŞ TAKSİMİ", u"KÜŞAT", u"1. SELAM", u"2. SELAM", u"3. SELAM", u"4. SELAM",
               u"TERENNÜM"]

kodlist = []
koddict = dict()

printflag = 0

tuplet = 0
capitals = []

#errLog = open('errLog.txt', 'w')
missingUsuls = []


def getNoteType(note, type, pay, payda, sira):
    global tuplet

    ## NEW PART FOR DOTTED NOTES
    temp_payPayda = float(pay) / int(payda)

    if temp_payPayda >= 1.0:
        type.text = 'whole'
        temp_undotted = 1.0
    elif 1.0 > temp_payPayda >= 1.0 / 2:
        type.text = 'half'
        temp_undotted = 1.0 / 2
    elif 1.0 / 2 > temp_payPayda >= 1.0 / 4:
        type.text = 'quarter'
        temp_undotted = 1.0 / 4
    elif 1.0 / 4 > temp_payPayda >= 1.0 / 8:
        type.text = 'eighth'
        temp_undotted = 1.0 / 8
    elif 1.0 / 8 > temp_payPayda >= 1.0 / 16:
        type.text = '16th'
        temp_undotted = 1.0 / 16
    elif 1.0 / 16 > temp_payPayda >= 1.0 / 32:
        type.text = '32nd'
        temp_undotted = 1.0 / 32
    elif 1.0 / 32 > temp_payPayda >= 1.0 / 64:
        type.text = '64th'
        temp_undotted = 1.0 / 64

    # check for tuplets
    if temp_payPayda == 1.0 / 12:
        type.text = 'eighth'
        temp_undotted = 1.0 / 12
        tuplet += 1
    elif temp_payPayda == 1.0 / 24:
        type.text = '16th'
        temp_undotted = 1.0 / 24
        tuplet += 1
    # end of tuplets

    # not tuplet, normal or dotted
    # print(tuplet)

    # print(temp_payPayda)

    nofdots = 0
    timemodflag = 0
    if tuplet == 0:
        # print(sira, temp_payPayda, temp_undotted)
        temp_remainder = temp_payPayda - temp_undotted

        dotVal = temp_undotted / 2.0
        while temp_remainder > 0:
            type = etree.SubElement(note, 'dot')
            nofdots += 1
            temp_remainder = temp_payPayda - temp_undotted - dotVal
            dotVal += dotVal / 2
            break
            # print(sira, temp_payPayda, temp_undotted, dotVal, temp_remainder)

    ##END OF NEW PART FOR DOTTED NOTES
    else:
        timemodflag = 1

    return timemodflag

    # print(sira, temp_payPayda, '------------------')


def getUsul(usul, file):
    fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'makams_usuls', 'usuls_v3_ANSI.txt')

    usulID = []
    usulName = []
    nofBeats = []
    beatType = []
    accents = []

    f = open(fpath)

    while 1:
        temp_line = f.readline()

        if len(temp_line) == 0:
            break
        else:
            temp_line = temp_line.split('\t')
            temp_line.reverse()
            # print(temp_line)

            try:
                usulID.append(temp_line.pop())
            except:
                usulID.append('')

            try:
                usulName.append(temp_line.pop())
            except:
                usulName.append('')

            try:
                nofBeats.append(temp_line.pop())
            except:
                nofBeats.append('')

            try:
                beatType.append(temp_line.pop())
            except:
                beatType.append('')

            try:
                accents.append(temp_line.pop())
            except:
                accents.append('')

    f.close()
    # eof file read
    '''
	print(usulID[usulID.index(usul)])
	print(usulName)
	print(nofBeats[usulID.index(usul)])
	print(beatType[usulID.index(usul)])
	print(accents)
	print(len(usulID),len(usulName),len(nofBeats),len(beatType),len(accents))
	'''
    try:
        # print( nofBeats[usulID.index(usul)], 2**int(beatType[usulID.index(usul)]) )
        return int(nofBeats[usulID.index(usul)]), int(
            beatType[usulID.index(usul)])  # second paramater, usul_v1 2**int(beatType[usulID.index(usul)]
    except:
        # print('Usul: ', usul, ' not in list')
        # errLog.write('Usul: ' + usul + ' not in list.\n')
        missingUsuls.append(usul + '\t' + file)
        # return 4, 4


def getAccName(alter):
    # print('Alter: ',alter)
    if alter in ['+1', '+2']:
        accName = d_koma
    elif alter in ['+3', '+4']:
        accName = d_bakiyye
    elif alter in ['+5', '+6']:
        accName = d_kmucennep
    elif alter in ['+7', '+8']:
        accName = d_bmucennep
    elif alter in ['-1', '-2']:
        accName = b_koma
    elif alter in ['-3', '-4']:
        accName = b_bakiyye
    elif alter in ['-5', '-6']:
        accName = b_kmucennep
    elif alter in ['-7', '-8']:
        accName = b_bmucennep

    return accName


def getKeySig(piecemakam, keysig):
    #print(piecemakam)
    makamTree = etree.parse(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'makams_usuls', 'Makamlar.xml'))

    xpression = '//dataroot/Makamlar[makam_adi= $makam]/'
    makam_ = piecemakam

    makamName = makamTree.xpath(xpression + 'Makam_x0020_Adi', makam=makam_)
    # print(makamName)

    donanim = []
    trToWestern = {'La': 'A', 'Si': 'B', 'Do': 'C', 'Re': 'D', 'Mi': 'E', 'Fa': 'F', 'Sol': 'G'}

    for i in range(1, 10):
        try:
            donanim.append((makamTree.xpath(xpression + 'Donanim-' + str(i), makam=makam_))[0].text)
            # print(donanim, i)
            for key, value in trToWestern.iteritems():
                donanim[-1] = donanim[-1].replace(key, value)
                # donanim[-1] = trToWestern[donanim[-1][:2]] + donanim[-1][2:]
                # print(donanim[-1], i)
        except:
            continue

    # print(makamName[0].text)
    # print(donanim)

    while len(donanim) > 0:
        temp_key = donanim.pop()
        # print(temp_key)
        if type(temp_key) != type(None):
            temp_key = temp_key.replace('#', '+')
            temp_key = temp_key.replace('b', '-')

            keystep = etree.SubElement(keysig, 'key-step')
            keystep.text = temp_key[0]
            # ''' alteration is not working for microtones
            keyalter = etree.SubElement(keysig, 'key-alter')
            keyalter.text = temp_key[-2:]
            # '''
            keyaccidental = etree.SubElement(keysig, 'key-accidental')
            keyaccidental.text = getAccName(temp_key[-2:])


class symbtrscore(object):
    def __init__(self, txtpath, mu2path, symbtrname='', mbid='', verbose=None):
        self.txtpath = txtpath  # filepath for the txt score
        self.mu2path = mu2path  # filepath for the mu2 score; used for obtaining the metadata from its header
        self.mbid = mbid  # musicbrainz unique identifier

        if verbose is None:
            verbose = False
        self.verbose = verbose

        if not symbtrname:
            self.symbtrname = os.path.splitext(os.path.basename(self.txtpath))[0]
        else:
            self.symbtrname = symbtrname

        # piece attributes
        self.makam = ""
        self.form = ""
        self.usul = ""
        self.name = ""
        self.composer = ""
        self.lyricist = ""
        self.mu2header = dict()
        self.mblink = []

        self.keysignature = []
        self.timesignature = []

        self.notes = []
        self.notecount = 0
        self.measures = []
        self.tempo = None
        self.mu2beatnumber = None
        self.mu2beattype = None

        self.tuplet = 0
        self.tupletseq = []

        self.score = None
        self.sections = []
        self.scorenotes = []
        self.sectionsextracted = dict()
        self.capitals = []
        self.phraseboundaryinfo = 0
        self.subdivisionthreshold = 0

        self.readsymbtr()  # read symbtr txt file

        self.symbt2xmldict = dict()

        # xml attribute flags
        self.xmlnotationsflag = 0
        self.xmlgraceslurflag = 0
        self.xmlglissandoflag = 0

    def printnotes(self):
        for e in self.notes:
            # pass
            print(vars(e))

    def sectionextractor(self):
        data, isDataValid = extractor.extract(self.txtpath, symbtrname=self.symbtrname,
                                              extract_all_labels=True, print_warnings=False)
        self.mu2header, headerRow, isHeaderValid = symbtrreader.readMu2Header(self.mu2path)
        # data = extractor.merge(txtdata, Mu2header)
        for item in data['sections']:
            self.sectionsextracted[item['startNote']] = item['name']
        # print(self.mu2header)
        mu2title = self.mu2header['title']['mu2_title']
        if mu2title is None:
            mu2title = self.mu2header['makam']['mu2_name'] + self.mu2header['usul']['mu2_name']

        mu2composer = self.mu2header['composer']['mu2_name']
        mu2lyricist = self.mu2header['lyricist']['mu2_name']

        self.mu2composer = mu2composer
        self.mu2lyricist = mu2lyricist
        self.mu2beatnumber = self.mu2header['usul']['number_of_pulses']
        self.mu2beattype = self.mu2header['usul']['mertebe']
        self.name = mu2title

    def addmbidlink(self):
        if self.mbid:
            try:  # single dict
                self.mblink.append("https://musicbrainz.org/" + self.mbid['type'] + '/' + self.mbid['mbid'])
            except TypeError:  # list
                for mbid in self.mbid:
                    self.mblink.append("https://musicbrainz.org/" + mbid['type'] + '/' + mbid['mbid'])

    def readsymbtr(self):
        finfo = self.symbtrname.split('--')
        finfo[-1] = finfo[-1][:-4]

        self.makam = finfo[0]
        self.form = finfo[1]
        self.usul = finfo[2]
        self.name = finfo[3]

        if self.name == "":
            self.name = self.makam + " " + self.form

        try:
            self.composer = finfo[4]
        except:
            self.composer = 'N/A'

        # makam = makam.replace('_',' ').title()
        # form = form.replace('_',' ').title()
        # usul = usul.replace('_',' ').title()
        self.name = self.name.replace('_', ' ').title()
        self.composer = self.composer.replace('_', ' ').title()

        self.sectionextractor()
        self.addmbidlink()

        self.readsymbtrlines()
        self.notecount = len(self.notes)
        # print(self.notecount)

    def readsymbtrlines(self):
        global kodlist, koddict

        f = open(self.txtpath)
        i = 0
        sumlinelength = 0
        temp_line = f.readline()

        # read operation
        while 1:
            temp_line = f.readline()  # column headers line
            # print(temp_line)
            if len(temp_line) == 0:
                break
            else:
                temp_line = temp_line.split('\t')
                # print(temp_line)
                self.notes.append(symbtrnote.note(temp_line, verbose=self.verbose))  # NOTE CLASS
                # print(vars(self.notes[-1]))

                if self.notes[-1].pay in ['51']:
                    if self.notes[-1].pay in ['5', '10']:  # seperating notes
                        temppay = int(self.notes[-1].pay)
                        # print("Note splitting:", temppay)
                        del self.notes[-1]
                        firstpart = temppay * 2 / 5
                        lastpart = temppay - firstpart

                        temp_line[6] = str(firstpart)
                        self.notes.append(symbtrnote.note(temp_line, verbose=self.verbose))
                        temp_line[6] = str(lastpart)
                        temp_line[11] = '_'
                        self.notes.append(symbtrnote.note(temp_line, verbose=self.verbose))
                    elif self.notes[-1].pay in ['9', '11']:
                        temppay = int(self.notes[-1].pay)
                        # print("Note splitting:", temppay)
                        del self.notes[-1]

                        temp_line[6] = str(3)
                        self.notes.append(symbtrnote.note(temp_line, verbose=self.verbose))
                        temp_line[6] = str(temppay - 3)
                        temp_line[11] = '_'
                        self.notes.append(symbtrnote.note(temp_line, verbose=self.verbose))

                if self.notes[-1].rest == 1 and self.notes[-1].pay == '0':  # removing rests with 0 duration
                    if self.verbose:
                        print("Warning! Note deleted. Rest with Pay:0. Sira:", self.notes[-1].sira)
                    del self.notes[-1]
                # DONE READING

                lastnote = self.notes[-1]
                if lastnote.graceerror == 1 and self.verbose:
                    print("\tgrace error:", lastnote.sira, lastnote.kod, lastnote.pay, lastnote.payda)
                # CHECK POINTS
                """
                if self.notes[-1].rest == 1 and self.notes[-1].dot == 1:
                    print("Rest with dot! Sira:", self.notes[-1].sira)
                if self.notes[-1].rest == 1 and  5>len(self.notes[-1].lyric) > 2:
                    print("Rest with lyric! Sira:", self.notes[-1].sira, self.notes[-1].lyric)
                if lastnote.dot > 0:
                    print("Dot", lastnote.dot, lastnote.sira)
                if lastnote.tuplet > 0:
                    print("Tuplet", lastnote.tuplet, lastnote.sira)
                    #print(self.txtpath, "note time", temppay, self.l_pay[-1], self.l_pay[-2], self.l_sira[-1], "AAAAAAAAAAAAAAAA")
                if lastnote.pay == '0' and lastnote.kod != '8':
                    print("DURATION ERROR:", self.txtpath, lastnote.sira, lastnote.kod, lastnote.pay)
                """

                if lastnote.kod in koddict:
                    koddict[lastnote.kod] += 1
                else:
                    koddict[lastnote.kod] = 1

                self.scorenotes.append(self.notes[-1].kod)
                kodlist.append(self.scorenotes[-1])

        kodlist = list(set(kodlist))
        if '53' in self.scorenotes:
            self.phraseboundaryinfo = 1
        # print("Kods used:", kodlist)
        # print("Koddict:", koddict)

        f.close()
        # eof file read
        # print ('sumlinelength:')
        # print(sumlinelength)
        # print(l_soz1)

        # cumulative time array

    def symbtrtempo(self, pay1, ms1, payda1, pay2, ms2, payda2):
        bpm = None
        try:
            bpm = 60000 * 4 * int(pay1) / (int(ms1) * int(payda1))
        except:
            bpm = 60000 * 4 * int(pay2) / (int(ms2) * int(payda2))
        self.tempo = bpm
        return bpm

    def addwordinfo(self, xmllyric, templyric, word, e):
        # lyrics word information
        if len(templyric) > 0 and templyric != "." and templyric not in sectionList:
            # print(spacechars)
            syllabic = etree.SubElement(xmllyric, 'syllabic')
            if e.syllabic is not None and word == 1:
                syllabic.text = "end"
                word = 0
            else:
                if word == 0 and (e.wordend or e.lineend):
                    syllabic.text = "single"
                    word = 0
                elif word == 0:
                    syllabic.text = "begin"
                    word = 1
                    # print("word start", cnt)
                elif word == 1:
                    syllabic.text = "middle"
                    # print("word middle", cnt)
        # print(templyric, endlineflag, word, spacechars)
        return word

    def addduration(self, xmlduration, e):
        temp_duration = int(self.nof_divs * 4 * int(e.pay) / int(e.payda))
        xmlduration.text = str(temp_duration)

        return temp_duration  # duration calculation	UNIVERSAL

    def addaccidental(self, xmlnote, xmlpitch, e):
        if e.accidental not in [None]:
            accidental = etree.SubElement(xmlnote, 'accidental')  # accidental XML create
            # print acc
            accidental.text = e.accidental
            '''
            alter = etree.SubElement(pitch, 'alter')
            if int(acc) > 0:
                alter.text = '1'
            else:
                alter.text = '-1'
            '''
            self.addalter(xmlpitch, e)

    def addalter(self, xmlpitch, e):
        if e.alter is not None:
            alter = etree.SubElement(xmlpitch, 'alter')
            alter.text = e.alter

    def adddot(self, xmlnote, e):
        # adding dots
        for i in range(0, e.dot):
            xmldot = etree.SubElement(xmlnote, 'dot')
            if self.verbose:
                print("DOT ADDED", e.sira)

    def addtuplet(self, xmlnote, e):
        global tuplet
        tuplet += 1

        self.tupletseq.append(int(e.payda))
        if tuplet > 1:
            if self.tupletseq[-2] != self.tupletseq[-1]:
                tuplet += 1

        time_mod = etree.SubElement(xmlnote, 'time-modification')
        act_note = etree.SubElement(time_mod, 'actual-notes')
        act_note.text = '3'
        norm_note = etree.SubElement(time_mod, 'normal-notes')
        norm_note.text = '2'

        xmlnotat = etree.SubElement(xmlnote, 'notations')
        self.xmlnotationsflag = 1

        if self.verbose:
            print("Tuplet added.", tuplet, e.tuplet, e.sira)
        # check for tuplets
        if tuplet == 1:
            tupletstart = etree.SubElement(xmlnotat, 'tuplet')
            tupletstart.set('type', 'start')
            tupletstart.set('bracket', 'yes')
        elif tuplet == 2:
            pass
        elif tuplet == 3:
            tupletstop = etree.SubElement(xmlnotat, 'tuplet')
            tupletstop.set('type', 'stop')
            # tupl.set('bracket', 'yes')
            tuplet = 0
            if self.verbose:
                print("Tuplet sequence:", self.tupletseq)
            self.tupletseq = []

        return xmlnotat

    def addtimemodification(self, note):
        global tuplet
        time_mod = etree.SubElement(note, 'time-modification')
        act_note = etree.SubElement(time_mod, 'actual-notes')
        act_note.text = '3'
        norm_note = etree.SubElement(time_mod, 'normal-notes')
        norm_note.text = '2'

        if tuplet == 1:
            notat = etree.SubElement(note, 'notations')
            tupletstart = etree.SubElement(notat, 'tuplet')
            tupletstart.set('type', 'start')
            tupletstart.set('bracket', 'yes')
        elif tuplet == 3:
            notat = etree.SubElement(note, 'notations')
            tupletstop = etree.SubElement(notat, 'tuplet')
            tupletstop.set('type', 'stop')
            # tupl.set('bracket', 'yes')
            tuplet = 0

    def addtremolo(self, xmlnotations, e):
        xmlornaments = etree.SubElement(xmlnotations, 'ornaments')
        xmltremolo = etree.SubElement(xmlornaments, 'tremolo')
        xmltremolo.set('type', 'single')
        xmltremolo.text = "2"
        if self.verbose:
            print("Tremolo added.", e.sira, e.kod)

    def addglissando(self, xmlnotations, e):
        if self.xmlglissandoflag == 1:
            xmlglissando = etree.SubElement(xmlnotations, 'glissando')
            xmlglissando.set('type', 'stop')
            self.xmlglissandoflag = 0
            if self.verbose:
                print("Glissando stop. Flag:", self.xmlglissandoflag, e.sira, e.kod, e.lyric)
        if e.glissando == 1:
            xmlglissando = etree.SubElement(xmlnotations, 'glissando')
            xmlglissando.set('line-type', 'wavy')
            xmlglissando.set('type', 'start')
            self.xmlglissandoflag = 1

            if self.verbose:
                print("Glissando start. Flag:", self.xmlglissandoflag, e.sira, e.kod, e.lyric)

    def addtrill(self, xmlnotations, e):
        xmlornaments = etree.SubElement(xmlnotations, 'ornaments')
        xmltrill = etree.SubElement(xmlornaments, 'trill-mark')
        xmltrill.set('placement', 'above')

        if self.verbose:
            print("Trill added.", e.sira, e.kod)

    def addgrace(self, xmlnote, e):
        grace = etree.SubElement(xmlnote, 'grace')  # note pitch XML create
        if self.xmlgraceslurflag > 0:
            grace.set('steal-time-previous', '10')
        else:
            grace.set('steal-time-following', '10')

    def addgraceslur(self, xmlnotations, e):
        if self.xmlgraceslurflag == 2:
            xmlgraceslur = etree.SubElement(xmlnotations, 'slur')
            xmlgraceslur.set('type', 'start')
            self.xmlgraceslurflag = 1
        else:
            xmlgraceslur = etree.SubElement(xmlnotations, 'slur')
            xmlgraceslur.set('type', 'stop')
            self.xmlgraceslurflag = 0

        if self.verbose:
            print("Grace slur flag:", self.xmlgraceslurflag)

    def addmordent(self, xmlnotations, e):
        xmlornaments = etree.SubElement(xmlnotations, 'ornaments')
        xmlmordent = etree.SubElement(xmlornaments, 'mordent')
        xmlmordent.set('placement', 'above')

        if e.mordentlower == 1:
            self.addlowermordent(xmlmordent)
            # pass

        if self.verbose:
            print("Mordent added.", e.sira, e.kod)

    def addinvertedmordent(self, xmlnotations, e):
        xmlornaments = etree.SubElement(xmlnotations, 'ornaments')
        xmlinvertedmordent = etree.SubElement(xmlornaments, 'inverted-mordent')
        xmlinvertedmordent.set('placement', 'below')

        if e.mordentlower == 1:
            self.addlowermordent(xmlinvertedmordent)
            # pass

        if self.verbose:
            print("Inverted Mordent added.", e.sira, e.kod)

    def addgrupetto(self, xmlnotations, e):
        xmlornaments = etree.SubElement(xmlnotations, 'ornaments')
        xmlturn = etree.SubElement(xmlornaments, 'turn')

        if self.verbose:
            print("Grupetto added.", e.sira, e.kod)

    def addlowermordent(self, xmlmordent):
        xmlmordent.set('approach', 'below')
        xmlmordent.set('departure', 'above')

    def usulchange(self, measure, tempatts, temppay, temppayda, nof_divs, templyric):
        nof_beats = int(temppay)
        beat_type = int(temppayda)
        measureLength = nof_beats * nof_divs * (4 / float(beat_type))
        # print(nof_beats, beat_type)
        # print(measureSum)
        time = etree.SubElement(tempatts, 'time')
        beats = etree.SubElement(time, 'beats')
        beatType = etree.SubElement(time, 'beat-type')
        beats.text = str(nof_beats)
        beatType.text = str(beat_type)

        # 1st measure direction: usul and makam info
        #						tempo(metronome)
        direction = etree.SubElement(measure, 'direction')
        direction.set('placement', 'above')
        directionType = etree.SubElement(direction, 'direction-type')

        # usul info
        words = etree.SubElement(directionType, 'words')
        words.set('default-y', '35')
        if templyric:
            words.text = 'Usul: ' + templyric.title()

        return measureLength

    def setsection(self, tempmeasurehead, lyric, templyric):
        if templyric != "SAZ":
            tempheadsection = tempmeasurehead.find(".//lyric")
        else:
            tempheadsection = lyric
        tempheadsection.set('name', templyric)

    def countcapitals(self, str):
        global capitals
        if str.isupper():
            capitals.append(str)

    def convertsymbtr2xml(self, verbose=None):
        if verbose is not None:
            self.verbose = verbose

        outkoddict = dict((e, 0) for e in kodlist)
        global tuplet
        tuplet = 0

        ###CREATE MUSIC XML
        # init
        self.score = etree.Element("score-partwise")  # score-partwise
        self.score.set('version', '3.0')

        # work-title
        work = etree.SubElement(self.score, 'work')
        workTitle = etree.SubElement(work, 'work-title')
        workTitle.text = self.name.title()

        # identification
        xmlidentification = etree.SubElement(self.score, 'identification')
        xmlcomposer = etree.SubElement(xmlidentification, 'creator')
        xmlcomposer.set('type', 'composer')
        xmlcomposer.text = self.mu2composer
        if len(self.mu2lyricist) > 0:
            xmllyricist = etree.SubElement(xmlidentification, 'creator')
            xmllyricist.set('type', 'poet')
            xmllyricist.text = self.mu2lyricist

        for idlink in self.mblink:
            xmlrelation = etree.SubElement(xmlidentification, 'relation')
            xmlrelation.text = idlink

        # part-list
        partList = etree.SubElement(self.score, 'part-list')
        scorePart = etree.SubElement(partList, 'score-part')
        scorePart.set('id', 'P1')
        partName = etree.SubElement(scorePart, 'part-name')
        partName.text = 'Music'

        # part1
        P1 = etree.SubElement(self.score, 'part')
        P1.set('id', 'P1')

        # measures array
        measure = []
        i = 1  # measure counter
        measureSum = 0
        subdivisioncounter = 0
        measuredelim = "-"

        # part1 measure1
        measure.append(etree.SubElement(P1, 'measure'))
        measure[-1].set('number', str(i) + measuredelim + str(subdivisioncounter))

        # 1st measure direction: usul and makam info
        #						tempo(metronome)
        direction = etree.SubElement(measure[-1], 'direction')
        direction.set('placement', 'above')
        directionType = etree.SubElement(direction, 'direction-type')

        # usul and makam info
        words = etree.SubElement(directionType, 'words')
        words.set('default-y', '35')
        words.text = 'Makam: ' + self.mu2header['makam']['mu2_name'] + ', Usul: ' + self.mu2header['usul']['mu2_name']

        # tempo info
        tempo = self.symbtrtempo(self.notes[1].pay, self.notes[1].ms, self.notes[1].payda,
                                 self.notes[2].pay, self.notes[2].ms, self.notes[2].payda)

        sound = etree.SubElement(direction, 'sound')
        sound.set('tempo', str(tempo))
        # print('tempo '+ str(tempo))

        nof_divs = 96
        self.nof_divs = nof_divs
        nof_beats = 4
        beat_type = 4
        if self.usul not in ['serbest', 'belirsiz']:
            #nof_beats, beat_type = getUsul(self.usul, self.txtpath)
            nof_beats = self.mu2beatnumber
            beat_type = self.mu2beattype

            measureLength = nof_beats * nof_divs * (4 / float(beat_type))

            if nof_beats >= 20:
                if nof_beats % 4 == 0:
                    self.subdivisionthreshold = measureLength / (nof_beats / 4)
                elif nof_beats % 2 == 0:
                    self.subdivisionthreshold = measureLength / (nof_beats / 2)
                elif nof_beats % 3 == 0:
                    self.subdivisionthreshold = measureLength / (nof_beats / 3)

            if self.verbose:
                print("After long usul check:", measureLength, self.subdivisionthreshold, nof_beats)

        else:
            nof_beats = ''
            beat_type = ''
            measureLength = 1000

        # print(usul, measureLength)

        # ATTRIBUTES
        atts1 = etree.SubElement(measure[-1], 'attributes')
        divs1 = etree.SubElement(atts1, 'divisions')
        divs1.text = str(nof_divs)

        # key signature
        keysig = etree.SubElement(atts1, 'key')
        getKeySig(self.makam, keysig)
        # print(makam)

        time = etree.SubElement(atts1, 'time')
        if self.usul in ['serbest', 'belirsiz']:
            senzamisura = etree.SubElement(time, 'senza-misura')
        else:
            beats = etree.SubElement(time, 'beats')
            beatType = etree.SubElement(time, 'beat-type')
            beats.text = str(nof_beats)
            beatType.text = str(beat_type)

        # print(l_acc)

        ###LOOP FOR NOTES
        # notes
        word = 0
        sentence = 0
        tempsection = 0
        graceflag = 0
        tempatts = ""
        tempmeasurehead = measure[-1]

        if self.phraseboundaryinfo == 1:
            xmlgrouping = etree.SubElement(measure[-1], 'grouping')
            xmlgrouping.set('type', 'start')
            xmlfeature = etree.SubElement(xmlgrouping, 'feature')

        for e in self.notes:
            tempkod = e.kod
            tempsira = e.sira
            temppay = e.pay
            temppayda = e.payda
            tempstep = e.step
            tempacc = e.accidental
            tempoct = e.octave
            templyric = e.lyric

            self.xmlnotationsflag = 0

            if tempkod not in ['35', '50', '51', '53', '54', '55']:
                xmlnote = etree.SubElement(measure[-1], 'note')  # note	UNIVERSAL
                self.symbt2xmldict[e.sira] = xmlnote
                xmlnote.append(etree.Comment('symbtr_txt_note_index ' + e.sira))

                # kods cannot mapped to musicxml
                if e.littlenote == 1:
                    xmlnote.append(etree.Comment(
                        'Warning! SymbTr_Kod: 1 Little note.  MusicXML schema does not have a appropriate mapping, treating the note as a normal note'))
                if e.silentgrace == 1:
                    xmlnote.append(etree.Comment(
                        'Warning! SymbTr_Kod: 11 Silent grace. MusicXML schema does not have a appropriate mapping, treating the note as a normal note'))

                if e.grace == 1:
                    outkoddict['8'] += 1
                    self.addgrace(xmlnote, e)
                    if self.xmlgraceslurflag == 0:
                        self.xmlgraceslurflag = 2
                elif e.pregrace == 1:
                    outkoddict['10'] += 1
                    self.xmlgraceslurflag = 2
                    # print("Kod 10.", e.sira)
                else:
                    pass

                if e.rest == 0:
                    outkoddict['9'] += 1
                    pitch = etree.SubElement(xmlnote, 'pitch')  # note pitch XML create
                else:
                    outkoddict['9'] += 1
                    xmlrest = etree.SubElement(xmlnote, 'rest')  # note rest XML create	REST

                if e.grace == 0:
                    xmlduration = etree.SubElement(xmlnote, 'duration')  # note duration XML create	UNIVERSAL
                    xmltype = etree.SubElement(xmlnote, 'type')  # note type XML create	UNIVERSAL
                # print(l_kod[cnt+1], l_nota[cnt] , l_payda[cnt+1])
                # print(l_payda[cnt+1])
                # BAŞLA
                if int(temppayda) == 0:
                    # print("Payda: 0", e.kod, e.sira, e.lyric)
                    temp_duration = 0
                    # continue
                else:
                    temp_duration = self.addduration(xmlduration, e)  # duration calculation	UNIVERSAL
                    xmltype.text = e.type
                    self.adddot(xmlnote, e)
                    # print(e.sira, e.type)

                if e.rest == 0:
                    step = etree.SubElement(pitch, 'step')  # note pitch step XML create
                    step.text = tempstep  # step val #XML assign

                    self.addaccidental(xmlnote, pitch, e)
                    # accidental.text = tempacc

                    octave = etree.SubElement(pitch, 'octave')  # note pitch octave XML create
                    octave.text = tempoct  # octave val XML assign

                if e.tuplet == 1:
                    outkoddict['9'] += 1
                    # print("tuplet var! xmlconverter func")
                    # print("NOTATFLAG:", self.xmlnotationsflag)
                    xmlnotations = self.addtuplet(xmlnote, e)
                    # print("NOTATFLAG:", self.xmlnotationsflag)
                    if e.tremolo == 1 or e.glissando == 1:
                        if self.verbose:
                            print("Tuplet with tremolo or glissando.")
                if e.tremolo == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for tremolo.")
                    self.addtremolo(xmlnotations, e)
                if e.glissando == 1 or self.xmlglissandoflag == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for glissando.")
                    self.addglissando(xmlnotations, e)
                if e.trill == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for trill.")
                    self.addtrill(xmlnotations, e)
                if e.mordent == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for mordent.")
                    self.addmordent(xmlnotations, e)
                if e.invertedmordent == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for inverted mordent.", e.sira, e.kod, e.invertedmordent)
                    self.addinvertedmordent(xmlnotations, e)
                if e.grupetto == 1:
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for grupetto/turn.", e.sira, e.kod, e.invertedmordent)
                    self.addgrupetto(xmlnotations, e)

                if self.xmlgraceslurflag > 0 and 0:  # disabled temporarily
                    if not xmlnote.find('notations'):
                        xmlnotations = etree.SubElement(xmlnote, 'notations')
                        if self.verbose:
                            print("Notations is added for grace.")
                    self.addgraceslur(xmlnotations, e)

                # LYRICS PART
                xmllyric = etree.SubElement(xmlnote, 'lyric')
                word = self.addwordinfo(xmllyric, templyric, word, e)  # word keeps the status of current syllable
                # current lyric text
                xmltext = etree.SubElement(xmllyric, 'text')
                xmltext.text = templyric

                # xmltext.text = e.sira if int(e.sira)%50 == 0 else xmltext.text #print note order mod50

                self.countcapitals(templyric)

                if e.lineend == 1:
                    endline = etree.SubElement(xmllyric, 'end-line')

                    # print(cnt, endlineflag, measureSum)

                # section information
                if int(tempsira) in self.sectionsextracted.keys():  # instrumental pieces and pieces with section keywords
                    # self.setsection(tempmeasurehead, xmllyric, templyric)
                    tempsection = self.sectionsextracted[int(tempsira)]
                    # print("extracted section", tempsira, tempsection)
                    xmllyric.set('name', tempsection)
                    self.sections.append(tempsection)

                measureSum += temp_duration
                # print(temp_duration, ' ', measureSum, ' ' , measureLength,' ',i)

                # NEW MEASURE
                if measureSum >= measureLength:
                    # print(e.sira, i)
                    # print(measureSum, measureLength)
                    subdivisioncounter = 0
                    i = int(i + 1)
                    measure.append(etree.SubElement(P1, 'measure'))
                    measure[-1].set('number', str(i) + measuredelim + str(subdivisioncounter))
                    tempatts = etree.SubElement(measure[-1], 'attributes')
                    measureSum = 0
                    tempmeasurehead = measure[-1]
                    # eof notes

                elif self.subdivisionthreshold != 0 and measureSum % self.subdivisionthreshold == 0 and 0:  # disabled temporarily
                    # print(measureSum, measureLength)
                    subdivisioncounter += 1
                    measure.append(etree.SubElement(P1, 'measure'))
                    measure[-1].set('number', str(i) + measuredelim + str(subdivisioncounter))
                    tempatts = etree.SubElement(measure[-1], 'attributes')

                    xmlbarline = etree.SubElement(measure[-1], 'barline')
                    xmlbarline.set('location', 'left')
                    xmlbarstyle = etree.SubElement(xmlbarline, 'bar-style')
                    xmlbarstyle.text = 'dashed'

            elif tempkod == '51':
                # print('XX')
                if e.sira == '1':
                    if self.verbose:
                        print("Initial usul is already set.")
                else:
                    try:
                        measureLength = self.usulchange(measure[-1], tempatts, temppay, temppayda, nof_divs, templyric)
                    except:
                        if self.verbose:
                            print('Kod', tempkod, 'but no time information.', e.sira, e.kod)

            elif tempkod == '50':
                if self.verbose:
                    print("makam change", self.txtpath, tempsira)
            # print(measure)
            elif tempkod == '35':
                if self.verbose:
                    print("Measure repetition.", e.sira)
                P1.remove(measure[-1])  # remove empty measure
                del measure[-1]

                xmeasure = copy.deepcopy(measure[-1])
                xmeasure.set('number', str(i))
                if xmeasure.find('direction') is not None:
                    xmeasure.remove(xmeasure.find('direction'))
                if xmeasure.find('attributes') is not None:
                    tempatts = xmeasure.find('attributes')
                    tempatts.clear()
                #this part will be active after musescore supports measure repetation
                # xmlmeasurestyle = etree.SubElement(tempatts, 'measure-style')
                # xmlmeasurerepeat = etree.SubElement(xmlmeasurestyle, 'measure-repeat')
                # xmlmeasurerepeat.set('type', 'start')
                # xmlmeasurerepeat.text = '1'
                P1.append(xmeasure)  # add copied measure to the score
                # print(etree.tostring(xmeasure))
                measure[-1] = xmeasure

                i += 1
                measure.append(etree.SubElement(P1, 'measure'))
                measure[-1].set('number', str(i))
                tempatts = etree.SubElement(measure[-1], 'attributes')
                measureSum = 0
                tempmeasurehead = measure[-1]

            elif tempkod == '53':  # phrase boundaries
                xmlgrouping = etree.SubElement(measure[-1], 'grouping')
                xmlgrouping.set('type', 'stop')
                xmlfeature = etree.SubElement(xmlgrouping, 'feature')
                xmlfeature.set('type', 'phrase')

                # print(self.notes.index(e), len(self.notes)-1)
                if self.notes.index(e) != len(self.notes) - 1:
                    xmlgrouping = etree.SubElement(measure[-1], 'grouping')
                    xmlgrouping.set('type', 'start')
                    xmlfeature = etree.SubElement(xmlgrouping, 'feature')
                    xmlfeature.set('type', 'phrase')

            elif tempkod == '54':  # flavors
                xmlgrouping = etree.SubElement(measure[-1], 'grouping')
                xmlgrouping.set('type', 'start')
                xmlfeature = etree.SubElement(xmlgrouping, 'feature')
                xmlfeature.set('type', 'flavor')
            elif tempkod == '55':  # flavours
                xmlgrouping = etree.SubElement(measure[-1], 'grouping')
                xmlgrouping.set('type', 'stop')
                xmlfeature = etree.SubElement(xmlgrouping, 'feature')
                xmlfeature.set('type', 'flavor')
        
        return self.getxmlstr()

    def getxmlstr(self): 
        return etree.tostring(self.score, pretty_print=True, xml_declaration=True, encoding="UTF-8", standalone=False,
            doctype='<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">')

    def writexml(self, outpath):
        # printing xml file
        f = open(outpath, 'wb')
        f.write(self.getxmlstr())
        f.close()

#errLog.write('\n'.join(set(missingUsuls)))
#errLog.write('\n' + str(len(set(missingUsuls))))
#errLog.close()

#f = open('capitals.txt', 'w')
#for item in set(capitals):
#    f.write(item.encode('utf8') + '\n')
#f.close()
