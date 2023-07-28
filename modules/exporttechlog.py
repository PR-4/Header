import csv
import re

unitDict = {}
descDict = {}
exportUnit  = True	# Properties units are exported if exportUnit is True
exportDescr = True	# Properties descriptions are exported if exportDescr is True

regexpsToRemove = []
if EXPORTSUMMARIES == "NO":
	regexpsToRemove.append(re.compile("^result_.*$"))
if EXPORTALIASES == "NO":
	regexpsToRemove.append(re.compile("^Alias_.*$"))

for w in db.wellList():
	for p in db.wellPropertyList(w):
		ok = True
		for r in regexpsToRemove:
			if r.match(p):
				ok = False
				break

		if ok:
			# Export Unit
			if exportUnit:
				pu = db.wellPropertyUnit(w, p)

				if p in unitDict:
					if not db.unitIsEquivalent(pu, unitDict[p]):
						print("<font color='orange'>Warning the property <b>'{0}'</b> is already defined in unit <b>'{1}'</b> and inside the well <b>'{2}'</b> is defined to be <b>'{3}'</b></font>".format(p, unitDict[p], w, pu))
						exportUnit = False
				else:
					unitDict[p] = pu
			else:
				unitDict[p] = ''

			# Export Description
			if exportDescr:
				pdescr = db.wellPropertyDescription(w, p)
				descDict[p] = pdescr
			else:
				descDict[p] = ''

		else:
			print("The property '{0}' will be skipped".format(p))

unitList = sorted(unitDict.keys())

if not unitList:
	print("No property found")
else:
	with open(fileName, "w", newline="",encoding = 'utf-8-sig') as csvFile:
		wnCol = "#WellPropertyName"
		writer = csv.DictWriter(csvFile, [wnCol] + unitList)

		#Write the headers
		#Next line can be updated by writer.writeheaders() with python 2.7
		writer.writerow(dict((fn,fn) for fn in writer.fieldnames))

		#Write the units
		unitLine = {wnCol:"#WellPropertyUnit"}
		if exportUnit:
			unitLine.update(unitDict)
		writer.writerow(unitLine)

		#Write the descriptions
		descLine = {wnCol:"#WellPropertyDescription"}
		if exportDescr:
			descLine.update(descDict)
		writer.writerow(descLine)

		#Write the properties values for all the wells
		for w in db.wellList():
			d = {wnCol:w}
			for p in db.wellPropertyList(w):
				ok = True
				for r in regexpsToRemove:
					if r.match(p):
						ok = False
						break
				if ok:
					d[p] = db.wellPropertyValue(w, p).replace("\r\n", "<TechNewLine>").replace('\n', "<TechNewLine>")
			writer.writerow(d)
	print("Done")