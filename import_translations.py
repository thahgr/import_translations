#!/usr/bin/python

import sys
import os
import pandas as pd
import shutil
import json
import re
from django.utils.encoding import smart_str, smart_unicode

if __name__ == "__main__":
	# a primitive menu
	if len(sys.argv) != 3 : 
		sys.exit("** Usage: ./import_translations xls_file path_to_res_folder **")

	# get excel file and path to res 
	file = sys.argv[1]
	path = sys.argv[2]

	excel = pd.read_excel(file, sheet_name=None, header=None)

	regex = re.compile('<string name="(.*?)">')

	# loop over tabs in the xls file, each tab is a language
	for lang, sheet in excel.items():

		# construct the target strings.xml file
		strings = path + "/values-" + lang + "/strings.xml"
		# print(strings)

		# copy the strings file into a backup, remove the original one
		backupFile = strings + ".orig"
		shutil.copy(strings,backupFile)
		os.remove(strings)

		# create a new file with the original name and read the backup
		out_file = open(strings, 'w')
		in_file = open(backupFile, 'r')

		# list with all existing keys for each language
		keysList = []

		for line in in_file:
			strLine = line.replace('\n', '')
			if(strLine != "</resources>"):
				out_file.write(line)
				m = regex.search(line)
				if m:
					keysList.append(m.group(1))
			else:

				# we found the end, loop over entries in the language sheet
				for i in range(len(sheet)) : 
					key = str(sheet.iloc[i,0])

					# if key already exists, skip it
					if key in keysList:
						continue

					english = str(sheet.iloc[i,1])
					try:
						translation = smart_str(sheet.iloc[i,2])
					except:
						continue

					# if for a chance translation is missing, skip
					if translation == 'nan':
						continue

					# sanitize translation, remove single quotes
					translation = translation.replace("'","\\'")
					translation = translation.replace("\\\\","\\")

					# form the translation string
					formattedLine = '    <string name="'+ key +'">' + translation + '</string>\n'
					# print(formattedLine)

					out_file.write(formattedLine)
				out_file.write(line)

		# cleanup
		out_file.close()
		in_file.close()
		os.remove(backupFile)

	print("\n### SUCCESS ###")


