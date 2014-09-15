def main():
	try:
		glob_import=False
		datetime_import=False
		et_import=False
		csv_import=False
		re_import=False
		pdb_import=False
		import glob
		glob_import=True
		import datetime
		datetime_import=True
		import xml.etree.ElementTree as et
#from lxml import etree as et
#libxml2
#libxslt
		et_import=True
		import csv
		csv_import=True
		import re
		re_import=True
		import pdb
		pdb_import=True
	except ImportError:
		print('Import Error detected!')
		print([['glob','datetime','et','csv','re','pdb'],[glob_import,datetime_import,et_import,csv_import,re_import,pdb_import]])
		if not pdb_import:
			return

	for file in glob.glob("*.gpx"):
		file_root=file[:-4]
		with open(file_root+'.csv','w',newline='') as csvfile:
			writer=csv.writer(csvfile,delimiter=",")
			writer.writerow(['Time','AltitudeMeters','LatitudeDegrees','LongitudeDegrees','HeartRateBpm','SecondsFromStart','DistanceTraveled'])
			f=et.parse(file)
			root=f.getroot()
			m=re.match(r'\{.*\}',root.tag)
			if m:
				ns=m.group(0)
			else:
				ns=''
			#pdb.set_trace()
			d0=False
			lat0=False
			long0=False
			dist=0
			for tp in root.findall('.//'+ns+'trkpt'):
				try:
					tp_time=tp.find(ns+'time').text
				except:
					tp_time=''
				try:
					tp_alt=tp.find(ns+'ele').text
				except:
					tp_alt=''
				try:
					tp_lat=tp.attrib['lat']
				except:
					tp_lat=''
				try:
					tp_long=tp.attrib['lon']
				except:
					tp_long=''
				try:
					tp_hr=tp.find(ns+'HeartRateBpm/'+ns+'Value').text #TODO
				except:
					tp_hr=''
				if len(tp_time) > 0:
					d=datetime.datetime.strptime(tp_time, '%Y-%m-%dT%H:%M:%SZ')
					if not d0:
						d0=d
						d_diff=datetime.timedelta(0)
					else:
						d_diff=d-d0
				else:
					d_diff=datetime.timedelta(0)
				if len(tp_lat) > 0 and len(tp_long) > 0:
					lat=float(tp_lat)
					long=float(tp_long)
					if not lat0:
						lat0=lat
						long0=long
						dist=0
					else:
						dist=dist+distance_on_earth(lat0,long0,lat,long)
						lat0=lat
						long0=long
				writer.writerow([tp_time,tp_alt,tp_lat,tp_long,tp_hr,d_diff.total_seconds(),dist])
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
