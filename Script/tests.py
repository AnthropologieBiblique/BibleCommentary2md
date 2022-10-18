#!/usr/bin/env python3


import os
import csv
import markdownify
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
import fileinput

AT = [
["Gn",1,50,"Genèse"],
["Ex",1,40,"Exode"],
["Lv",1,27,"Lévitique"],
["Nb",1,36,"Nombres"],
["Dt",1,34,"Deutéronome"],
["Jos",1,24,"Josué"],
["Jg",1,21,"Juges"],
["Rt",1,4,"Ruth"],
["1S",1,31,"1 Samuel"],
["2S",1,24,"2 Samuel"],
["1R",1,22,"1 Rois"],
["2R",1,25,"2 Rois"],
["1Ch",1,29,"1 Chroniques"],
["2Ch",1,36,"2 Chroniques"],
["Esd",1,10,"Esdras"],
["Ne",1,13,"Néhémie"],
["Tb",1,14,"Tobie"],
["Jdt",1,16,"Judith"],
["Est",0,10,"Esther"],
["1M",1,16,"1 Martyrs"],
["2M",1,15,"2 Martyrs"],
["Jb",1,42,"Job"],
["Pr",1,31,"Proverbes"],
["Qo",1,12,"Ecclésiaste"],
["Ct",1,8,"Cantique"],
["Sg",1,19,"Sagesse"],
["Si",0,51,"Ecclesiastique"],
["Is",1,66,"Isaïe"],
["Jr",1,52,"Jérémie"],
["Lm",1,5,"Lamentations"],
["Ba",1,5,"Baruch"],
["Ez",1,48,"Ezekiel"],
["Dn",1,14,"Daniel"],
["Os",1,14,"Osée"],
["Jl",1,4,"Joël"],
["Am",1,9,"Amos"],
["Ab",0,0,"Abdias"],
["Jon",1,4,"Jonas"],
["Mi",1,7,"Michée"],
["Na",1,3,"Nahum"],
["Ha",1,3,"Habaquc"],
["So",1,3,"Sophonie"],
["Ag",1,2,"Aggée"],
["Za",1,14,"Zacharie"],
["Ml",1,3,"Malachie"]
]

NT = [
["Mt",1,28,"Évangile selon saint Matthieu"],
["Mc",1,16,"Évangile selon saint Marc"],
["Lc",1,24,"Évangile selon saint Luc"],
["Jn",1,21,"Évangile selon saint Jean"],
["Ac",1,28,"Actes des Apôtres"],
["Rm",1,16,"Épître aux Romains"],
["1Co",1,16,"Première épître aux Corinthiens"],
["2Co",1,13,"Deuxième épître aux Corinthiens"],
["Ga",1,6,"Épître aux Galates"],
["Ep",1,6,"Épître aux Ephésiens"],
["Ph",1,4,"Épître aux Philippiens"],
["Col",1,4,"Épître aux Colossiens"],
["1Th",1,5,"Première épître aux Thessaloniciens"],
["2Th",1,3,"Deuxième épître aux Thessaloniciens"],
["1Tm",1,6,"Première épître à Timothée"],
["2Tm",1,4,"Deuxième épître à Timothée"],
["Tt",1,3,"Épître à Tite"],
["Phm",1,1,"Épître à Philémon"],
["He",1,13,"Épître aux Hébreux"],
["Jc",1,5,"Épître de saint Jacques"],
["1P",1,5,"Première épître de saint Pierre"],
["2P",1,3,"Deuxième épître de saint Pierre"],
["1Jn",1,5,"Première épître de saint Jean"],
["2Jn",1,1,"Deuxième épître de saint Jean"],
["3Jn",1,1,"Troisième épître de saint Jean"],
["Jude",1,1,"Épître de saint Jude"],
["Ap",1,22,"Apocalypse"]
]

PS = [
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8",
"9A",
"9B",
"10",
"11",
"12",
"13",
"14",
"15",
"16",
"17",
"18",
"19",
"20",
"21",
"22",
"23",
"24",
"25",
"26",
"27",
"28",
"29",
"30",
"31",
"32",
"33",
"34",
"35",
"36",
"37",
"38",
"39",
"40",
"41",
"42",
"43",
"44",
"45",
"46",
"47",
"48",
"49",
"50",
"51",
"52",
"53",
"54",
"55",
"56",
"57",
"58",
"59",
"60",
"61",
"62",
"63",
"64",
"65",
"66",
"67",
"68",
"69",
"70",
"71",
"72",
"73",
"74",
"75",
"76",
"77",
"78",
"79",
"80",
"81",
"82",
"83",
"84",
"85",
"86",
"87",
"88",
"89",
"90",
"91",
"92",
"93",
"94",
"95",
"96",
"97",
"98",
"99",
"100",
"101",
"102",
"103",
"104",
"105",
"106",
"107",
"108",
"109",
"110",
"111",
"112",
"113A",
"113B",
"114",
"115",
"116",
"117",
"118",
"119",
"120",
"121",
"122",
"123",
"124",
"125",
"126",
"127",
"128",
"129",
"130",
"131",
"132",
"133",
"134",
"135",
"136",
"137",
"138",
"139",
"140",
"141",
"142",
"143",
"144",
"145",
"146",
"147",
"148",
"149",
"150"
]

def telechargerVersets(livre, chapitre):
	# Téléchargement d'un chapitre de la bible AELF sur aelf.org/bible
	try:
	    url = "https://www.aelf.org/bible/"+livre+"/"+chapitre
	    headers = {}
	    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	    req = urllib.request.Request(url, headers = headers)
	    resp = urllib.request.urlopen(req)
	    respData = resp.read().decode('utf-8')
	    saveFile = open('temp.html','w')
	    saveFile.write(str(respData))
	    saveFile.close()
	except Exception as e:
	    print(str(e))
	
	# Ouverture du html pour parsing
	file = open('temp.html', 'r')
	contents = file.read()
	soup = BeautifulSoup(contents, 'html.parser')
	
	for data in soup.find_all():
		if data.name == "p":
			if data.attrs == {}:
				print(data.contents[0].getText())
				print(data.contents[1])

telechargerVersets("Gn","1")
telechargerVersets("Ps","100")

for i in range(1,1+1):
	print(i)
