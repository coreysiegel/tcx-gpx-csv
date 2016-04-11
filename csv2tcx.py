import re
import sys
import argparse
import string
import pdb

# takes in a TCX file and outputs a CSV file
def main (input, output):
	fin=open(input, 'r')
	fout=open(output, 'w')
	row_id=0
	skipNext=False
	for line in fin:
		row_id+=1
		s=line.strip().split(',')
		if row_id==1:
			columns=s
			numColumns=len(columns)
		else:
			fout.write('<Trackpoint>\n')
			for i in range(0, len(s)):
				if skipNext:
					skipNext=False
				elif columns[i]=='LatitudeDegrees' or columns[i]=='LongitudeDegrees':
					fout.write('<Position>\n'+ \
							'<'+columns[i]+'>'+s[i]+'</'+columns[i]+'>\n'+ \
							'<'+columns[i+1]+'>'+s[i+1]+'</'+columns[i+1]+'>\n'+ \
							'</Position>\n')
					skipNext=True
				elif columns[i]=='heartratebpm/value':
					fout.write('<HeartRateBpm>\n')
					fout.write('<Value>'+s[i]+'</Value>\n')
					fout.write('</HeartRateBpm>\n')
				else:
					fout.write('<'+columns[i]+'>'+s[i]+'</'+columns[i]+'>\n')
			fout.write('</Trackpoint>\n')
	fout.close()
	fin.close()

if __name__=='__main__':
	# arguments
	parser = argparse.ArgumentParser(description=
		'something.')
	parser.add_argument('input', help='input CSV file')
	parser.add_argument('output', help='output TCX file')
	#parser.add_argument('--verbose', help='increase output verbosity', action='store_true')
	args = parser.parse_args()
	
	main(args.input, args.output)
