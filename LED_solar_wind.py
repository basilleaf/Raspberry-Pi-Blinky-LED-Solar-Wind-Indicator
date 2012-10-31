import RPi.GPIO as GPIO
import time
import urllib2

# for now we are manually guessing at endpoints, based on perusing the data. Tweak these:
wind_speed_endpoints = (260.,380.) # x1, x2
blink_delay_endpoints = (2., .05)  # y1, y2

url = 'http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt'

# the real offset should be 60 i think but noticing the data actually changes in shorter increments *shrug* 
offset = 30  # offset in seconds 

# initiate the LED
GPIO.setup(11, GPIO.OUT)

def blink(wind_speed):
	blink_delay = get_blink_delay(wind_speed,wind_speed_endpoints,blink_delay_endpoints)
	GPIO.output(11, True)
	time.sleep(blink_delay)
	GPIO.output(11, False)
	time.sleep(blink_delay)

def get_blink_delay(wind_speed,wind_speed_endpoints,blink_delay_endpoints):
	# want to find blink delay that corresponds inversely with solar wind speed
	# so when solar wind speed increases blink speed increases
	# blink delay is time between ON and OFF and corresponds inversely with blink speed
	# so doing this with a negative linear slope between 2 points on a plane (my WAG at an approach)
	# where x axis = wind speed and y axis = blink speed
	# find the equation of the slope between the 2 points then 
	# when given wind_speed solve for y to get blink delay:

	# but first: have we bursted from our expected range? adjust!
	if wind_speed < wind_speed_endpoints[0]:
		wind_speed_endpoints[0] = wind_speed
		print "new min wind_speed = " + wind_speed
	if wind_speed > wind_speed_endpoints[1]:
		wind_speed_endpoints[1] = wind_speed
		print "new max wind_speed = " + wind_speed

	# solving for y.. 
	(x1, x2) = wind_speed_endpoints  # points on an x-y graph
	(y1, y2) = blink_delay_endpoints
	m = (y2-y1)/(x2-x1) # slope = rise/run
	blink_delay = m*(wind_speed - x1) + y1 # equation of a stright line bt 2 points: y-y1 = m(x-x1) maths! 
	return blink_delay

consecutive_urlib_errors = 0
while True:
	# grab the page
	try:
		page_lines =  urllib2.urlopen(url)
	except:
		# got a 404, wait a sec and try again, only try a few times before bailing
		consecutive_urlib_errors += 1
		if consecutive_urlib_errors < 3: time.sleep(5)
		else: time.sleep(20) # start waiting a little longer if it fails 3+ times
		if consecutive_urlib_errors < 7:
			print 'url failed, waiting a sec and trying again..'
			continue  
		else: 
			raise Exception("url failed 7 times in a row, turning off")

	consecutive_urlib_errors = 0
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
	for obs in my_science_data:

		wind_speed = float(obs['Bulk_wind_speed'])

		"""
		print obs
		print wind_speed
		print get_blink_delay(wind_speed,wind_speed_endpoints,blink_delay_endpoints)
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






