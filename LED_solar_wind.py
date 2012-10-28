import RPi.GPIO as GPIO
import time
import urllib2


# initiate the LED
GPIO.setup(11, GPIO.OUT)

def slow():
	t = 2.1
	GPIO.output(11, True)
	time.sleep(t)
	GPIO.output(11, False)
	time.sleep(t)

def medium():
	t = .7
	GPIO.output(11, True)
	time.sleep(t)
	GPIO.output(11, False)
	time.sleep(t)

def fast():
	t = .3
	GPIO.output(11, True)
	time.sleep(t)
	GPIO.output(11, False)
	time.sleep(t)

while True:
	# grab the page
	try:
		page_lines =  urllib2.urlopen('http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt')
	except:
		raise Exception("Http 404 - invalid start url: " + start_url)

	# grab the data from the page
	my_science_data = []
	for line in page_lines:
		if (line.find('#') == 0) | (line.find(':') == 0):
			continue # this line is commented out

		# this is data!
		data = line.split()

		"""
		my_science_data += [{
							'YR':data[0], 	
							'DA' : data[1],
							'HHMM' : data[2],
							'JDAY' : data[3],
							'SDAY' : data[4],
							'S' : data[5],
							'Proton_Density' : data[6],
							'Bulk_Speed' : data[7],
							'Ion_Temp' : data[8]
							}]
		"""
		try:
			my_science_data.append({'SDAY': data[-5], 'Bulk_Speed' : data[-2] })
		except IndexError:	
			pass
	page_lines.close()

	# start the sequence
	offset = 10 # seconds - the real offset is 60
	for obs in my_science_data:

		speed = float(obs['Bulk_Speed'])
		print obs
		print speed

		now = time.time()
		future = now + offset

		if speed < 340:
			while True:
				slow()
				if time.time() > future:
					break			
		elif speed < 347:
			while True:
				medium()
				if time.time() > future:
					break			
		elif speed > 346:
			while True:
				fast()
				if time.time() > future:
					break			






