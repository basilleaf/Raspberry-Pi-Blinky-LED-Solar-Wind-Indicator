import RPi.GPIO as GPIO
import time
import urllib2

# initiate the LED
GPIO.setup(11, GPIO.OUT)

def blink(wind_speed):
	blink_delay = get_blink_delay(wind_speed)
	GPIO.output(11, True)
	time.sleep(blink_delay)
	GPIO.output(11, False)
	time.sleep(blink_delay)

def get_blink_delay(wind_speed):
	# want to find blink delay that corresponds inversely with wind wind_speed
	# so when wind wind_speed increases blink wind_speed increases
	# blink delay is time between ON and OFF and corresponds inversely with solar wind wind_speed
	# so doing this with a negative linear slope between 2 points on a plane (my WAG at an approach)
	# where x axis = wind wind_speed and y axis = blink wind_speed
	# find the equation of the slope between the 2 points then 
	# when given wind_speed solve for y to get blink delay:

	# for now we are manually guessing at endpoints, based on perusing the data:
	wind_speed_endpoints = (260.,325) # x1, x2
	blink_delay_endpoints = (2., .05)  # y1, y2

	# solve for y to get blink delay
	(x1, x2) = wind_speed_endpoints  # points on an x-y graph
	(y1, y2) = blink_delay_endpoints
	m = (y2-y1)/(x2-x1) # slope = rise/run
	blink_delay = m*(wind_speed - x1) + y1 # y-y1 = m(x-x1) maths! 
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
			my_science_data.append({'SDAY': data[-5], 'Bulk_wind_speed' : data[-2] })
			page_lines.close()
			break # we only want the first real data entry
		except IndexError:	
			pass

	# start the sequence
	
	# the real offset should be 60 but noticing the data actually changes in shorter increments *shrug* 
	# so hitting the data feed page every 20 seconds.. 
	offset = 20  # offset in seconds - 
	for obs in my_science_data:

		wind_speed = float(obs['Bulk_wind_speed'])

		"""
		print obs
		print wind_speed
		print get_blink_delay(wind_speed)
		"""
		now = time.time()
		future = now + offset

		if wind_speed == -9999.9: # this is their null, just turn off the LED..
			GPIO.output(11, False)
			time.sleep(int(offset/2))
			break

		while True:
			blink(wind_speed)
			if time.time() > future:
				break			






