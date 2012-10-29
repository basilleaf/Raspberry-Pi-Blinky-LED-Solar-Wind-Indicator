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

		try:
			my_science_data.append({'SDAY': data[-5], 'Bulk_Speed' : data[-2] })
			page_lines.close()
			break # we only want the first real data entry
		except IndexError:	
			pass

	# start the sequence
	offset = 60 # seconds - the real offset is 60
	for obs in my_science_data:

		speed = float(obs['Bulk_Speed'])
		print obs
		print speed

		now = time.time()
		future = now + offset

		if speed == -9999.9: # this is their null, turn it off..
			GPIO.output(11, False)
			time.sleep(int(offset/2))
			break

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






