"""
	Blink an LED at speeds that correspond with real time solar wind speed
	wind speed data here: http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt
	For the Raspberry Pi.
"""
import RPi.GPIO as GPIO
import time
import urllib2

# initiate the LED
GPIO.setup(11, GPIO.OUT)

def blink(speed):
	blink_delay = find_blink_delay(speed)
	GPIO.output(11, True)
	time.sleep(blink_delay)
	GPIO.output(11, False)
	time.sleep(blink_delay)

def find_blink_delay(wind_speed):
	# want to find blink delay that corresponds inversely with wind speed
	# so when wind speed increases blink delay becomes proportionally smaller
	# so doing this with a negative linear slope between 2 points on a plane (my WAG at an approach)
	# where x axis = wind speed and y axis = blink speed
	# so find the equation of the slope between xmin, ymin and xmax, ymax
	# so then when given wind_speed you just solve for y to get blink deley:

	# for now we are manually guessing at endpoints, based on perusing the data:
	wind_speed_endpoints = (300.,360) # x1, x2
	blink_delay_endpoints = (2., .1)  # y1, y2

	# solve for y to get blink delay
	(x1, x2) = wind_speed_endpoints  # points on an x-y graph
	(y1, y2) = blink_delay_endpoints
	m = (y2-y1)/(x2-x1) # slope
	blink_delay = m*(wind_speed - x1) + y1
	return blink_delay

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
	offset = 20 # seconds - the real offset is 60
	for obs in my_science_data:

		speed = float(obs['Bulk_Speed'])
		print obs
		print speed
		print find_blink_delay(speed)

		now = time.time()
		future = now + offset

		if speed == -9999.9: # this is their null, turn it off..
			GPIO.output(11, False)
			time.sleep(int(offset/2))
			break

		while True:
			blink(speed)
			if time.time() > future:
				break			






