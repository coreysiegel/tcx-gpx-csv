import re
import sys
import argparse
import string
import pdb
import xml.etree.ElementTree as et

# takes in a TCX file and outputs a CSV file
def main (input, output):
	tree = et.parse(input)
	root = tree.getroot()
	m=re.match(r'^({.*})', root.tag)
	if m:
		ns=m.group(1)
	else:
		ns=''
	if root.tag!=ns+'TrainingCenterDatabase':
		print('Unknown root found: '+root.tag)
		return
	activities=root.find(ns+'Activities')
	if not activities:
		print('Unable to find Activities under root')
		return
	activity=activities.find(ns+'Activity')
	if not activity:
		print('Unable to find Activity under Activities')
		return
	columnsEstablished=False
	for lap in activity.iter(ns+'Lap'):
		if columnsEstablished:
			fout.write('New Lap\n')
		for track in lap.iter(ns+'Track'):
			#pdb.set_trace()
			if columnsEstablished:
				fout.write('New Track\n')
			for trackpoint in track.iter(ns+'Trackpoint'):
				try:
					time=trackpoint.find(ns+'Time').text.strip()
				except:
					time=''
				try:
					latitude=trackpoint.find(ns+'Position').find(ns+'LatitudeDegrees').text.strip()
				except:
					latitude=''
				try:
					longitude=trackpoint.find(ns+'Position').find(ns+'LongitudeDegrees').text.strip()
				except:
					longitude=''
				try:
					altitude=trackpoint.find(ns+'AltitudeMeters').text.strip()
				except:
					altitude=''
				try:
					bpm=trackpoint.find(ns+'HeartRateBpm').find(ns+'Value').text.strip()
				except:
					bpm=''
				if not columnsEstablished:
					fout=open(output, 'w')
					fout.write(','.join(('Time','LatitudeDegrees','LongitudeDegrees','AltitudeMeters','heartratebpm/value'))+'\n')
					columnsEstablished=True
				fout.write(','.join((time,latitude,longitude,altitude,bpm))+'\n')

	fout.close()

if __name__=='__main__':
	# arguments
	parser = argparse.ArgumentParser(description=
		'something.')
	parser.add_argument('input', help='input TCX file')
	parser.add_argument('output', help='output CSV file')
	#parser.add_argument('--verbose', help='increase output verbosity', action='store_true')
	args = parser.parse_args()
	
	main(args.input, args.output)
