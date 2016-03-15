# -*- coding: utf-8 -*-
import sys

# koma definitions
# flats
b_koma = 'quarter-flat'  # 'flat-down'
b_bakiyye = 'slash-flat'
b_kmucennep = 'flat'
b_bmucennep = 'double-slash-flat'
# sharps
d_koma = 'quarter-sharp'  # quarter-sharp, SWAP 1ST AND 3RD SHARPS
d_bakiyye = 'sharp'
d_kmucennep = 'slash-quarter-sharp'  # slash-quarter-sharp
d_bmucennep = 'slash-sharp'

altervalues = {'quarter-flat': "-0.5", 'slash-flat': None, 'flat': '-1',
               'double-slash-flat': None, 'quarter-sharp': '+0.5',
               'slash-sharp': None, 'sharp': "+1", 'slash-quarter-sharp': None}

# section list
sectionList = [u"1. HANE", u"2. HANE", u"3. HANE", u"4. HANE", u"TESLİM",
               u"TESLİM ", u"MÜLÂZİME", u"SERHÂNE", u"HÂNE-İ SÂNİ",
               u"HÂNE-İ SÂLİS", u"SERHANE", u"ORTA HANE", u"SON HANE",
               u"1. HANEYE", u"2. HANEYE", u"3. HANEYE", u"4. HANEYE",
               u"KARAR", u"1. HANE VE MÜLÂZİME", u"2. HANE VE MÜLÂZİME",
               u"3. HANE VE MÜLÂZİME", u"4. HANE VE MÜLÂZİME",
               u"1. HANE VE TESLİM", u"2. HANE VE TESLİM",
               u"3. HANE VE TESLİM", u"4. HANE VE TESLİM", u"ARANAĞME",
               u"ZEMİN", u"NAKARAT", u"MEYAN", u"SESLERLE NİNNİ",
               u"OYUN KISMI", u"ZEYBEK KISMI", u"GİRİŞ SAZI",
               u"GİRİŞ VE ARA SAZI", u"GİRİŞ", u"FİNAL", u"SAZ", u"ARA SAZI",
               u"SUSTA", u"KODA", u"DAVUL", u"RİTM", u"BANDO", u"MÜZİK",
               u"SERBEST", u"ARA TAKSİM", u"GEÇİŞ TAKSİMİ", u"KÜŞAT",
               u"1. SELAM", u"2. SELAM", u"3. SELAM", u"4. SELAM", u"TERENNÜM"]


class Note(object):
    def __init__(self, info, verbose=None):
        # base attributes
        self.sira = None
        self.kod = None
        self.nota53 = None
        self.notaAE = None
        self.koma53 = None
        self.komaAE = None
        self.pay = None
        self.payda = None
        self.ms = None
        self.LNS = None
        self.velOn = None
        self.soz1 = None
        self.offset = None
        self.nof_divs = 0

        # xml attributes
        self.step = None  # get_pitch
        self.octave = None  # get_pitch
        self.duration = None
        self.type = None  # get_note_type
        self.accidental = None  # get_accidental
        self.alter = None  # get_accidental

        self.lyric = u''
        self.syllabic = None
        self.wordend = 0
        self.lineend = 0

        self.rest = 0  # get_rest
        self.grace = 0  # get_grace
        self.pregrace = 0
        self.dot = 0  # get_note_type
        self.tuplet = 0  # get_note_type
        self.tremolo = 0
        self.glissando = 0
        self.trill = 0
        self.mordent = 0
        self.invertedmordent = 0
        self.mordentlower = 0
        self.grupetto = 0
        self.littlenote = 0
        self.silentgrace = 0

        self.phraseend = 0

        self.graceerror = 0

        if verbose is None:
            verbose = False
        self.verbose = verbose
        self.fetchsymbtrinfo(info)

    def fetchsymbtrinfo(self, info):
        # print info
        self.sira = info[0]
        self.kod = info[1]
        self.nota53 = info[2]
        self.notaAE = info[3]
        self.koma53 = info[4]
        self.komaAE = info[5]
        self.pay = info[6]
        self.payda = info[7]
        self.ms = info[8]
        self.LNS = info[9]
        self.velOn = info[10]
        self.soz1 = info[11].decode('utf-8')
        self.offset = info[12]

        if self.kod not in ['35', '51', '53', '54', '55']:
            self.get_rest()
            self.get_grace()
            if self.grace == 1 and self.pay != '0':
                self.graceerror = 1

                if self.verbose:
                    print("Warning: GraceError! pay and payda has been "
                          "changed.", self.sira, self.kod, self.pay)

                self.pay = '0'
                self.payda = '0'
            if self.rest == 0:
                self.get_pitch()
            # BURASI DÜZELEECEK
            if self.grace == 0 and self.payda != '0' and self.kod != '0':
                self.get_note_type()
                self.get_accidental()
            self.get_word()

            # ornaments
            if self.kod == '1':
                self.littlenote = 1
            elif self.kod == '4':
                self.glissando = 1
            elif self.kod in ['7', '16']:
                self.tremolo = 1
            elif self.kod in ['12', '32']:
                self.trill = 1
            elif self.kod == '23':
                self.mordent = 1
            elif self.kod == '24':
                self.mordent = 1
                self.mordentlower = 1
            elif self.kod == '43':
                self.invertedmordent = 1
            elif self.kod == '44':
                self.invertedmordent = 1
                self.mordentlower = 1
            elif self.kod == '28':  # xml tag -> TURN
                self.grupetto = 1

        elif self.kod == '51':
            self.lyric = self.soz1

        elif self.kod == '53':  # phrase boundary
            self.phraseend = 1

    def get_rest(self):
        if self.kod == 0 or self.nota53 == "Es":
            self.rest = 1

    def get_grace(self):
        if self.kod == '8':
            self.grace = 1
        elif self.kod == '10':
            self.pregrace = 1
        elif self.kod == '11':
            self.silentgrace = 1

    def get_pitch(self):
        try:
            self.step = self.notaAE[0]
            self.octave = self.notaAE[1]
        except:
            if self.verbose:
                print(self.sira, self.notaAE, "get_pitch error")
            sys.exit(1)

    def get_note_type(self):
        # print(self.sira, self.kod, "symbtrnote.get_note_type")
        temp_pay_payda = float(self.pay) / int(self.payda)

        temp_undotted = None
        if temp_pay_payda >= 1.0:
            self.type = 'whole'
            temp_undotted = 1.0
        elif 1.0 > temp_pay_payda >= 1.0 / 2:
            self.type = 'half'
            temp_undotted = 1.0 / 2
        elif 1.0 / 2 > temp_pay_payda >= 1.0 / 4:
            self.type = 'quarter'
            temp_undotted = 1.0 / 4
        elif 1.0 / 4 > temp_pay_payda >= 1.0 / 8:
            self.type = 'eighth'
            temp_undotted = 1.0 / 8
        elif 1.0 / 8 > temp_pay_payda >= 1.0 / 16:
            self.type = '16th'
            temp_undotted = 1.0 / 16
        elif 1.0 / 16 > temp_pay_payda >= 1.0 / 32:
            self.type = '32nd'
            temp_undotted = 1.0 / 32
        elif 1.0 / 32 > temp_pay_payda >= 1.0 / 64:
            self.type = '64th'
            temp_undotted = 1.0 / 64

        # check for tuplets
        if temp_pay_payda == 1.0 / 6:
            self.type = 'quarter'
            temp_undotted = 1.0 / 6
            self.tuplet = 1
        elif temp_pay_payda == 1.0 / 12:
            self.type = 'eighth'
            temp_undotted = 1.0 / 12
            self.tuplet = 1
        elif temp_pay_payda == 1.0 / 24:
            self.type = '16th'
            temp_undotted = 1.0 / 24
            self.tuplet = 1
        # end of tuplets

        if self.tuplet == 0:
            temp_remainder = temp_pay_payda - temp_undotted
            dot_val = temp_undotted / 2.0
            while temp_remainder > 0:
                # print(temp_pay_payda, temp_undotted, temp_remainder,
                # self.sira, self.type)
                self.dot += 1
                temp_remainder = temp_pay_payda - temp_undotted - dot_val
                dot_val += dot_val / 2
            if self.dot > 1 and 0:
                if self.verbose:
                    print("Dots! 1 or more. #ofDots:", self.dot, self.sira)
            # print(sira, temp_pay_payda, temp_undotted, dot_val,
            # temp_remainder)

    def get_accidental(self):
        acc = self.notaAE[2:]
        if acc != '':
            if acc in ['#1', '#2']:
                self.accidental = d_koma
            elif acc in ['#3', '#4']:
                self.accidental = d_bakiyye
            elif acc in ['#5', '#6']:
                self.accidental = d_kmucennep
            elif acc in ['#7', '#8']:
                self.accidental = d_bmucennep
            elif acc in ['b1', 'b2']:
                self.accidental = b_koma
            elif acc in ['b3', 'b4']:
                self.accidental = b_bakiyye
            elif acc in ['b5', 'b6']:
                self.accidental = b_kmucennep
            elif acc in ['b7', 'b8']:
                self.accidental = b_bmucennep
            # print(self.sira)
            self.alter = altervalues[self.accidental]

    def get_word(self):
        if 1:  # self.soz1 not in section_list:
            self.lyric = self.soz1
            self.syllabic = ""  # remove NoneType
            if '  ' in self.lyric:  # line endings
                self.lineend = 1
                self.wordend = 1
            elif ' ' in self.lyric:  # word endings
                self.wordend = 1

            if self.lineend or self.wordend:
                self.syllabic = "end"
