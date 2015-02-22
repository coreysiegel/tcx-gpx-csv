def main():
	advanced_warning=150 # feet

	try:
		glob_import=False
		datetime_import=False
		decimal_import=False
		et_import=False
		csv_import=False
		re_import=False
		pdb_import=False
		import glob
		glob_import=True
		import datetime
		datetime_import=True
		decimal_import=True
		import xml.etree.ElementTree as et
		et_import=True
		import csv
		csv_import=True
		import re
		re_import=True
		import pdb
		pdb_import=True
	except ImportError:
		print('Import Error detected!')
		print([['glob', 'datetime', 'decimal', 'et', 'csv', 're', 'pdb'], [glob_import, datetime_import, decimal_import, et_import, csv_import, re_import, pdb_import]])
		if not pdb_import:
			return

	pdb.set_trace()
	for file in glob.glob("*.tcx"):
		print('Now processing '+file)
		file_root=file[:-4]
		with open(file_root+'_shift.tcx', 'w', newline='') as outfile:
			f=et.parse(file)
			root=f.getroot()
			m=re.match(r'\{.*\}', root.tag)
			if m:
				ns=m.group(0)
			else:
				ns=''
			#pdb.set_trace()
			d0=False
			cp_lat0=False
			cp_long0=False
			dist=0
			for cp in root.findall('.//'+ns+'CoursePoint'):
				try:
					cp_name=cp.find(ns+'Name').text
				except:
					cp_name=''
				try:
					cp_time=cp.find(ns+'Time').text
				except:
					cp_time=''
				try:
					cp_lat_str=cp.find(ns+'Position/'+ns+'LatitudeDegrees').text
				except:
					cp_lat_str=''
				try:
					cp_long_str=cp.find(ns+'Position/'+ns+'LongitudeDegrees').text
				except:
					cp_long_str=''
				try:
					cp_type=cp.find(ns+'PointType').text
				except:
					cp_type=''
				try:
					cp_note=cp.find(ns+'Notes').text
				except:
					cp_note=''

				if len(cp_lat) > 0 and len(cp_long) > 0:
					cp_lat=float(cp_lat_str)
					cp_long=float(cp_long_str)
					dist=0
					if not cp_lat0:
						cp_lat0=cp_lat
						cp_long0=cp_long
					else:
						if not (cp_lat0==cp_lat and cp_long0==cp_long):
							dist=distance_on_earth(cp_lat0, cp_long0, cp_lat, cp_long)
					if dist > 0: # give extra advanced warning
						if dist < advanced_warning:
							#TODO: give advance warning immediately after last turn
						else:
							#TODO: give advanced warning appopriate distance before identified turn
					cp_lat0=cp_lat
					cp_long0=cp_long

				writer.writerow([cp_time, cp_alt, cp_lat_str, cp_long_str, cp_hr, d_diff.total_seconds(), dist])
			csvfile.close()

import math

def distance_on_earth(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    earth_diameter_ft = 3960*5280
    return arc*earth_diameter_ft

if __name__ == '__main__':
	main()
