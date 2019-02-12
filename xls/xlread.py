import sys
import xlrd
fout = open("flightnew.xlsx","w")
data = xlrd.open_workbook('flight.xlsx')
table = data.sheet_by_name(u'label')
for line in range(8821):
	sen1 = table.cell(line,0).value
	#print(sen1)
	sen2 = table.cell(line,1).value
	#print(sen2)
	if sen2=="":
		fout.write(sen1.encode("utf-8")+"\n")
	else:
		fout.write(sen2.encode("utf-8")+"\n")


