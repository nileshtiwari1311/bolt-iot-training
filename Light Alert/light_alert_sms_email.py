import sms_conf, email_conf, json, time
from boltiot import Sms, Email, Bolt

min_limit = 400
max_limit = 800

mybolt = Bolt(sms_conf.API_KEY, sms_conf.DEVICE_ID)
sms = Sms(sms_conf.SID, sms_conf.AUTH_TOKEN, sms_conf.TO_NUMBER, sms_conf.FROM_NUMBER)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)

while True: 
	print ("Reading sensor value")
	response = mybolt.analogRead('A0') 
	data = json.loads(response) 
	print("Sensor value(intensity) is: " + str(data['value']))
	try: 
		sensor_value = int(data['value']) 
		if sensor_value > max_limit or sensor_value < min_limit:
			print("Making request to Bolt device to blink LED")
			print("Making request to Twilio to send a SMS")
			print("Making request to Mailgun to send an email")
			task0 = mybolt.digitalWrite('0', 'HIGH')
			task1 = sms.send_sms("The Current light intensity sensor value is " + str(sensor_value))
			task2 = mailer.send_email("Alert", "The Current light intensity sensor value is " + str(sensor_value))
			print("Response received from Bolt Device is: " + str(task0))
			print("Response received from Twilio is: " + str(task1))
			print("Status of SMS at Twilio is :" + str(task1.status))
			task2_text = json.loads(task2.text)
			print("Response received from Mailgun is: " + str(task2_text['message']))
			time.sleep(2)
			task0 = mybolt.digitalWrite('0', 'LOW')
	except Exception as e: 
		print ("Error occured: Below are the details")
		print (e)
	time.sleep(10)