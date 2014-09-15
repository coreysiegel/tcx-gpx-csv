def main():
	try:
		csv_import=False
		pdb_import=False
		import csv
		csv_import=True
		import pdb
		pdb_import=True
	except ImportError:
		print('Import Error detected!')
		print([['csv','pdb'],[csv_import,pdb_import]])
		if not pdb_import:
			return

	file='2014-07-06-08-08-54.tcx'
	file_root=file[:-4]

	time=0
	ele=1
	lat=2
	long=3
	hr=4

	with open(file_root+'.csv',newline='') as csvfile:
		with open(file,'w',newline='') as tcxfile:
			reader=csv.reader(csvfile,delimiter=',',quotechar='\'')
			for row in reader:
				if row[0][0:4]=='2014':
					tcxfile.write('          <Trackpoint>\n')
					tcxfile.write('            <Time>'+row[time]+'</Time>\n')
					if len(row[lat]) > 0 or len(row[long]) > 0:
						tcxfile.write('            <Position>\n')
						if len(row[lat]) > 0:
							tcxfile.write('              <LatitudeDegrees>'+row[lat]+'</LatitudeDegrees>\n')
						if len(row[long]) > 0:
							tcxfile.write('              <LongitudeDegrees>'+row[long]+'</LongitudeDegrees>\n')
						tcxfile.write('            </Position>\n')
					if len(row[ele]) > 0:
						tcxfile.write('            <AltitudeMeters>'+row[ele]+'</AltitudeMeters>\n')
					if len(row[hr]) > 0:
						tcxfile.write('            <HeartRateBpm xsi:type="HeartRateInBeatsPerMinute_t">\n')
						tcxfile.write('              <Value>'+row[hr]+'/Value>\n')
						tcxfile.write('            </HeartRateBpm>\n')
					tcxfile.write('          </Trackpoint>\n')
			tcxfile.close()
		csvfile.close()

if __name__ == '__main__':
	main()
