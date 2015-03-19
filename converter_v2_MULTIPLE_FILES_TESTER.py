import numpy
import matplotlib.pyplot as plt
import os
import fnmatch
import getopt
import sys
from types import *
from lxml import etree

#koma definitions
#flats
b_koma = 'quarter-flat' #'flat-down'
b_bakiyye = 'slash-flat'
b_kmucennep = 'flat'
b_bmucennep = 'double-slash-flat'

#sharps
d_koma = 'slash-quarter-sharp'
d_bakiyye = 'sharp'
d_kmucennep = ''
d_bmucennep = 'slash-sharp'

tuplet = 0

errLog = open('errLog.txt', 'w')
missingUsuls = []

def getNoteType(note, type, pay, payda, sira):
	global tuplet
	
	## NEW PART FOR DOTTED NOTES
	temp_payPayda = int(pay)/int(payda)
	
	if temp_payPayda >= 1:
		type.text = 'whole'
		temp_undotted = 1
	elif temp_payPayda >= 1/2:
		type.text = 'half'
		temp_undotted = 1/2
	elif temp_payPayda >= 1/4:
		type.text = 'quarter'
		temp_undotted = 1/4
	elif temp_payPayda >= 1/8:
		type.text = 'eighth'
		temp_undotted = 1/8
	elif temp_payPayda >= 1/16:
		type.text = '16th'
		temp_undotted = 1/16
	elif temp_payPayda >= 1/32:
		type.text = '32nd'
		temp_undotted = 1/32
	elif temp_payPayda >= 1/64:
		type.text = '64th'
		temp_undotted = 1/64
	
	#check for tuplets
	if temp_payPayda == 1/12:
		type.text = 'eighth'
		temp_undotted = 1/12
		tuplet += 1
	elif temp_payPayda == 1/24:
		type.text = '16th'
		temp_undotted = 1/24
		tuplet += 1
	#end of tuplets
	
	#not tuplet, normal or dotted
	#print(tuplet)
	print(temp_payPayda)
	if tuplet == 0:
		#print(sira, temp_payPayda, temp_undotted)
		temp_remainder = temp_payPayda - temp_undotted
		
		dotVal = temp_undotted/2
		while(temp_remainder > 0):
			type = etree.SubElement(note,'dot')
			temp_remainder = temp_payPayda - temp_undotted - dotVal
			dotVal += dotVal/2
		print(sira, temp_payPayda, temp_undotted, dotVal, temp_remainder)
		##END OF NEW PART FOR DOTTED NOTES
	else:
		time_mod = etree.SubElement(note, 'time-modification')
		act_note = etree.SubElement(time_mod, 'actual-notes')
		act_note.text = '3'
		norm_note = etree.SubElement(time_mod, 'normal-notes')
		norm_note.text = '2'
		
		if tuplet == 1:
			notat = etree.SubElement(note, 'notations')
			tupl = etree.SubElement(notat, 'tuplet')
			tupl.set('type', 'start')
			tupl.set('bracket', 'yes')
		elif tuplet == 3:
			notat = etree.SubElement(note, 'notations')
			tupl = etree.SubElement(notat, 'tuplet')
			tupl.set('type', 'stop')
			#tupl.set('bracket', 'yes')
			tuplet = 0
		
		print(sira, temp_payPayda, '------------------')

def getUsul(usul, file):

	fpath = 'C:\\Users\\Burak\\Desktop\\CompMusic\\Makamlar\\usuls_v3_ANSI.txt'
	
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
			#print(temp_line)			

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
			
	f.close
	#eof file read
	'''
	print(usulID[usulID.index(usul)])
	print(usulName)
	print(nofBeats[usulID.index(usul)])
	print(beatType[usulID.index(usul)])
	print(accents)
	print(len(usulID),len(usulName),len(nofBeats),len(beatType),len(accents))
	'''
	try:
		#print( nofBeats[usulID.index(usul)], 2**int(beatType[usulID.index(usul)]) )
		return int(nofBeats[usulID.index(usul)]), int(beatType[usulID.index(usul)]) #second paramater, usul_v1 2**int(beatType[usulID.index(usul)]
	except:
		#print('Usul: ', usul, ' not in list')
		#errLog.write('Usul: ' + usul + ' not in list.\n')
		missingUsuls.append(usul + '\t' + file)
		#return 4, 4

def getAccName(alter):
	#print('Alter: ',alter)
	if alter == '+1' or alter == '+2':
		accName = d_koma
	elif alter == '+4' or alter == '+3':
		accName = d_bakiyye
	elif alter == '+5' or alter == '+6':
		accName = d_kmucennep
	elif alter == '+8' or alter == '+7':
		accName = d_bmucennep
	elif alter == '-1' or alter == '-2':
		accName = b_koma
	elif alter == '-4' or alter == '-3':
		accName = b_bakiyye
	elif alter == '-5' or alter == '-6':
		accName = b_kmucennep
	elif alter == '-8' or alter == '-7':
		accName = b_bmucennep
		
	return accName

def getKeySig(piecemakam, keysig):
	makamTree = etree.parse('C:\\Users\\Burak\\Desktop\\CompMusic\\Makamlar\\Makamlar.xml')
	xpression = '//dataroot/Makamlar[makam_adi= $makam]/'
	makam_ = piecemakam

	makamName = makamTree.xpath(xpression+'Makam_x0020_Adı', makam = makam_)

	donanim = []

	for i in range(1,10):
		try:
			donanim.append((makamTree.xpath(xpression+'Donanım-'+str(i), makam = makam_))[0].text)
			if donanim[-1][:2] == 'La':
				donanim[-1] = 'A'+donanim[-1][2:]
			elif donanim[-1][:2] == 'Si':
				donanim[-1] = 'B'+donanim[-1][2:]
			elif donanim[-1][:2] == 'Do':
				donanim[-1] = 'C'+donanim[-1][2:]
			elif donanim[-1][:2] == 'Re':
				donanim[-1] = 'D'+donanim[-1][2:]
			elif donanim[-1][:2] == 'Mi':
				donanim[-1] = 'E'+donanim[-1][2:]
			elif donanim[-1][:2] == 'Fa':
				donanim[-1] = 'F'+donanim[-1][2:]
			elif donanim[-1][:3] == 'Sol':
				donanim[-1] = 'G'+donanim[-1][3:]
				
			#print(donanim[-1])
		except:
			break
			
	#print(makamName[0].text)
	#print(donanim)
	
	while len(donanim) > 0:
		temp_key = donanim.pop()
		#print(temp_key)
		if type(temp_key) != type(None):
			temp_key = temp_key.replace('#','+')
			temp_key = temp_key.replace('b','-')
			
			keystep = etree.SubElement(keysig, 'key-step')
			keystep.text = temp_key[0]
			''' alteration is not working for microtones
			keyalter = etree.SubElement(keysig, 'key-alter')
			keyalter.text = temp_key[-2:]
			'''
			keyaccidental = etree.SubElement(keysig, 'key-accidental')
			keyaccidental.text = getAccName(temp_key[-2:])

def txtToMusicXML(fpath):
	
	global tuplet
	tuplet = 0
	
	#column definitions
	l_sira =[]
	l_kod = []
	l_nota53 = []
	l_notaAE = []
	l_koma53 = []
	l_komaAE = []
	l_pay = []
	l_payda = []
	l_ms = []
	l_LNS = []
	l_velOn = []
	l_soz1 = []
	l_offset = []

	#file to be read
	#fpath = "araban--kupe_56_--musemmen--etse--ahmet_avni_konuk.txt"

	#finfo[0] makam
	#finfo[1] form
	#finfo[2] usul
	#finfo[3] name
	#finfo[4] composer
	finfo = fpath.split('--')
	finfo[-1] = finfo[-1][:-4]
	#print(finfo)
	#print(finfo[0],finfo[1],finfo[2],finfo[3],finfo[4])
	
	makam = finfo[0]
	form = finfo[1]
	usul = finfo[2]
	name = finfo[3]
	try:
		composer = finfo[4]
	except:
		composer = 'N/A'
	
	#makam = makam.replace('_',' ').title()
	#form = form.replace('_',' ').title()
	#usul = usul.replace('_',' ').title()
	name = name.replace('_',' ').title()
	composer = composer.replace('_',' ').title()
	
	f = open(fpath)
	i=0

	#read operation
	while 1:
		temp_line = f.readline()
		#print(temp_line)
		if len(temp_line) == 0:
			break
		elif len(temp_line.split('\t')) == 1:
			l_soz1[-1] = l_soz1[-1] + temp_line
		else:
			temp_line = temp_line.split('\t')
			temp_line.reverse()
			#print(temp_line)
			#print(len(temp_line))
			l_sira.append(temp_line.pop())
			l_kod.append(temp_line.pop())
			l_nota53.append(temp_line.pop())
			l_notaAE.append(temp_line.pop())
			l_koma53.append(temp_line.pop())
			l_komaAE.append(temp_line.pop())
			l_pay.append(temp_line.pop())
			l_payda.append(temp_line.pop())
			l_ms.append(temp_line.pop())
			l_LNS.append(temp_line.pop())
			l_velOn.append(temp_line.pop())
			try:
				l_soz1.append(temp_line.pop())
			except:
				l_soz1.append('')
			try:
				l_offset.append(temp_line.pop())
				l_offset[-1] = l_offset[-1][:-1]
			except:
				l_offset.append('')
			i+=1
	f.close
	#eof file read
			
	#cumulative time array
	l_time = [0]
	l_temp = list(l_ms)
	l_temp.reverse()
	l_temp.pop()

	while len(l_temp) != 0:
			l_time.append(l_time[-1] + int(l_temp.pop()))
	#eof time array
			
	#print(l_time)
	l_freq = list(l_komaAE)
	l_freq[0]=l_freq[1]

	'''
	#printing columns
	print(l_sira)
	print(l_kod)
	print(l_nota53)
	print(l_notaAE)
	print(l_koma53)
	print(l_komaAE)
	print(l_pay)
	print(l_payda)
	print(l_ms)
	print(l_LNS)
	print(l_velOn)
	print(l_soz1)
	print(l_offset)
	'''
	'''
	#plotting
	plt.step(l_time,l_freq)
	plt.show()
	'''
	
	l_nota=[]
	l_oct =[]
	l_acc =[]

	l_temp = list(l_notaAE)
	l_temp.reverse()
	l_temp.pop()

	while len(l_temp) != 0:
		temp_note = l_temp.pop()
		if(len(temp_note)>0 and temp_note != 'Sus' and temp_note != 'Es'):
			l_nota.append(temp_note[0])
			l_oct.append(temp_note[1])
			
			if len(temp_note) == 2:
				l_acc.append('')
			else:
				if temp_note[2] == '#':
					try:
						l_acc.append('+' + temp_note[3])
					except:
						print(temp_note)
				else:
					try:
						l_acc.append('-' + temp_note[3])
					except:
						print(temp_note)
		else:
			l_nota.append('r')
			l_oct.append('r')
			l_acc.append('r')
			
	'''
	print(len(l_notaAE))
	print(len(l_nota))
	print(len(l_oct))
	print(len(l_acc))
	'''

	'''
	#printing into file
	ttt=[]
	for cnt in range(0, len(l_nota)):
		ttt.append(l_nota[cnt] + l_oct[cnt] + l_acc[cnt])

	f = open("converted.txt","w")
	for item in ttt:
		f.write(item+"\n")
	f.close()
	'''

	###CREATE MUSIC XML
	from lxml import etree

	#init
	score = etree.Element("score-partwise")	#score-partwise
	score.set('version','3.0')

	#defaults PAGE LAYOUT
	'''
	defaults = etree.SubElement(score, 'defaults')
	pageLayout = etree.SubElement(defaults, 'page-layout')
	pageHeight = etree.SubElement(pageLayout, 'page-height')
	pageHeight.text = '594'
	pageWidth = etree.SubElement(pageLayout, 'page-width')
	pageWidth.text = '420'
	'''
	
	#work-title
	work = etree.SubElement(score, 'work')
	workTitle = etree.SubElement(work, 'work-title')
	workTitle.text = name.title()
	
	#part-list
	partList = etree.SubElement(score, 'part-list')
	scorePart = etree.SubElement(partList, 'score-part')
	scorePart.set('id','P1')
	partName = etree.SubElement(scorePart, 'part-name')
	partName.text = 'Music'

	#part1
	P1 = etree.SubElement(score, 'part')
	P1.set('id','P1')

	#measures array
	measure = []
	i = 1
	measureSum = 0

	#part1 measure1
	measure.append(etree.SubElement(P1, 'measure'))
	measure[-1].set('number',str(i))

	#1st measure direction: usul and makam info
	#						tempo(metronome)
	direction = etree.SubElement(measure[-1], 'direction')
	direction.set('placement', 'above')
	directionType = etree.SubElement(direction, 'direction-type')
	#usul and makam info
	words = etree.SubElement(directionType, 'words')
	words.set('default-y','35')
	words.text = 'Makam: ' + makam.title() +', Usul: ' + usul.title()
	#tempo info
	try:
		tempo = 60000*4*int(l_pay[1])/(int(l_ms[1])*int(l_payda[1]))
	except:
		tempo = 60000*4*int(l_pay[2])/(int(l_ms[2])*int(l_payda[2]))
	sound = etree.SubElement(direction, 'sound')
	sound.set('tempo', str(tempo))
	#print('tempo '+ str(tempo))

	nof_divs = 24
	nof_beats = 4 #4
	beat_type = 4 #4
	if(usul != 'serbest' and usul != 'belirsiz'):
		nof_beats, beat_type = getUsul(usul, fpath)
		measureLength = nof_beats * nof_divs * (4/beat_type)
	else:
		nof_beats = ''
		beat_type = ''
		measureLength = 1000
	
	#print(usul, measureLength)

	#ATTRIBUTES
	atts1 = etree.SubElement(measure[-1], 'attributes')
	divs1 = etree.SubElement(atts1, 'divisions')
	divs1.text = str(nof_divs)

	time = etree.SubElement(atts1, 'time')
	beats = etree.SubElement(time, 'beats')
	beatType = etree.SubElement(time, 'beat-type')
	beats.text = str(nof_beats)
	beatType.text = str(beat_type)

	#key signature
	keysig = etree.SubElement(atts1, 'key')
	getKeySig(makam, keysig)
	#print(makam)
	
	'''
	keystep = etree.SubElement(keysig, 'key-step')
	keystep.text = 'E'
	keyalter = etree.SubElement(keysig, 'key-alter')
	keyalter.text = '-1'
	keyaccidental = etree.SubElement(keysig, 'key-accidental')
	keyaccidental.text = 'slash-flat'
	'''
	
	###LOOP FOR NOTES
	#notes
	for cnt in range(0, len(l_nota)):
		if(l_kod[cnt+1] != '8' and l_kod[cnt+1] != '0' and l_kod[cnt+1] != '35' and l_kod[cnt+1] != '51'):
			if(l_nota[cnt] != 'r'):
				note = etree.SubElement(measure[-1],'note')	#note	UNIVERSAL

				pitch = etree.SubElement(note,'pitch')	#note pitch XML create
				duration = etree.SubElement(note,'duration')	#note duration XML create	UNIVERSAL
				type = etree.SubElement(note,'type')	#note type XML create	UNIVERSAL
				#print(l_kod[cnt+1], l_nota[cnt] , l_payda[cnt+1])
				#print(l_payda[cnt+1])
				if int(l_payda[cnt+1]) == 0:
					print(l_sira[cnt+1] +'\t'+ l_kod[cnt+1] +'\t'+ fpath)
					continue
				temp_duration = int(nof_divs*4 * int(l_pay[cnt+1]) / int(l_payda[cnt+1])) #duration calculation	UNIVERSAL
				duration.text = str(temp_duration)		#XML assign		UNIVERSAL
				
				'''
				if int(l_payda[cnt+1]) == 4: type.text = 'quarter'	#UNIVERSAL
				if int(l_payda[cnt+1]) == 8: type.text = 'eighth'	#UNIVERSAL
				if int(l_payda[cnt+1]) == 16: type.text = '16th'	#UNIVERSAL
				'''
				getNoteType(note, type, l_pay[cnt+1], l_payda[cnt+1], l_sira[cnt+1])

				step = etree.SubElement(pitch, 'step')	#note pitch step XML create
				step.text = l_nota[cnt]		#step val #XML assign
				octave = etree.SubElement(pitch, 'octave')	#note pitch octave XML create
				octave.text = l_oct[cnt]	#octave val XML assign
				
				#setting accidentals
				#sharps
				accidental = etree.SubElement(note, 'accidental')	#accidental XML create
				#print(cnt, ' ', len(l_acc))
				if l_acc[cnt] == '+1':
					accidental.text = d_koma
					alter = etree.SubElement(pitch, 'alter')	#note alter
					alter.text = '0.5'
				elif l_acc[cnt] == '+4':
					accidental.text = d_bakiyye
					alter = etree.SubElement(pitch, 'alter')	#note alter
					alter.text = '1'
				elif l_acc[cnt] == '+5':
					accidental.text = d_kmucennep
				elif l_acc[cnt] == '+8':
					accidental.text = d_bmucennep
				elif l_acc[cnt] == '-1':
					accidental.text = b_koma
					alter = etree.SubElement(pitch, 'alter')	#note alter
					alter.text = '-0.5'
				elif l_acc[cnt] == '-4':
					accidental.text = b_bakiyye
				elif l_acc[cnt] == '-5':
					accidental.text = b_kmucennep
					alter = etree.SubElement(pitch, 'alter')	#note alter
					alter.text = '-1'
				elif l_acc[cnt] == '-8':
					accidental.text = b_bmucennep
					
				lyric = etree.SubElement(note, 'lyric')
				text = etree.SubElement(lyric, 'text')
				text.text = l_soz1[cnt+1]
			else:
				note = etree.SubElement(measure[-1],'note')	#note	UNIVERSAL

				rest = etree.SubElement(note,'rest')	#note duration XML create	UNIVERSAL
				duration = etree.SubElement(note,'duration')	#note duration XML create	UNIVERSAL
				type = etree.SubElement(note,'type')	#note type XML create	UNIVERSAL
				#print(l_kod[cnt+1], l_nota[cnt] , l_payda[cnt+1])
				#print(l_payda[cnt+1])
				if int(l_payda[cnt+1]) == 0:
					print(l_sira[cnt+1] +'\t'+ l_kod[cnt+1] +'\t'+ fpath)
					continue
				temp_duration = int(nof_divs*4 * int(l_pay[cnt+1]) / int(l_payda[cnt+1])) #duration calculation	UNIVERSAL
				duration.text = str(temp_duration)		#XML assign		UNIVERSAL
				
				##OLD PART FOR NOTE TYPES
				'''
				if int(l_payda[cnt+1]) == 4: type.text = 'quarter'	#UNIVERSAL
				if int(l_payda[cnt+1]) == 8: type.text = 'eighth'	#UNIVERSAL
				if int(l_payda[cnt+1]) == 16: type.text = '16th'	#UNIVERSAL
				'''
				##END OF OLD PART FOR NOTE TYPES
				getNoteType(note, type, l_pay[cnt+1], l_payda[cnt+1], l_sira[cnt+1])
				
			measureSum += temp_duration
			#print(temp_duration, ' ', measureSum, ' ' , measureLength,' ',i)
			
			#NEW MEASURE	
			if measureSum >= measureLength:
				i += 1
				measure.append(etree.SubElement(P1, 'measure'))
				measure[-1].set('number',str(i))
				measureSum = 0
		#eof notes

	#printing xml file
	f = open(fpath[:-4]+'.xml','wb')
	f.write(etree.tostring(score, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype='<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'))
	f.close

def singleFile():
	txtToMusicXML('beyati--sarki--aksak--benzemez_kimse--fehmi_tokay.txt')

def multipleFiles():
	errorFiles = []
	totalFiles = 0
	cnvFiles = 0
	errFiles = 0
	
	for file in os.listdir('.'):
		if fnmatch.fnmatch(file, '*.txt') and file != 'errLog.txt' and file != 'errorFiles.txt':
			print(file)
			txtToMusicXML(file)
			totalFiles += 1
			'''
			try:
				txtToMusicXML(file)
				cnvFiles += 1
			except:
				errorFiles.append(file)
				errFiles += 1
			'''	
	f = open('errorFiles.txt', 'w')
	for item in errorFiles:
		f.write(item+'\n')
	f.close
	print('Total files: ', totalFiles)
	print('Converted: ', cnvFiles)
	print('Failed: ', errFiles)
	print('Usul Conflict: ', len(set(missingUsuls)))

#main
if sys.argv[1] == '1':
	singleFile()
else:
	multipleFiles()

errLog.write('\n'.join(set(missingUsuls)))
errLog.write('\n' + str(len(set(missingUsuls))))
errLog.close()