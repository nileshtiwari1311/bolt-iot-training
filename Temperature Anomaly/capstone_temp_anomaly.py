import email_conf, conf
from boltiot import Email, Bolt
import json, time, math, statistics

def compute_bounds(history_data, frame_size, factor):
    if len(history_data) < frame_size :
        return None

    if len(history_data) > frame_size :
        del history_data[0:len(history_data)-frame_size]

    Mn = statistics.mean(history_data)
    Variance = 0
    for data in history_data :
        Variance += math.pow((data-Mn),2)
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1] + Zn
    Low_bound = history_data[frame_size-1] - Zn
    return [High_bound, Low_bound]

min_limit = 123 #12 degree celsius 
max_limit = 140 #13.7 degree celsius

mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)
history_data = []

while True: 
    print ("Reading sensor value")
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print ("Sensor value is: " + str(data['value']))
    try: 
        sensor_value = int(data['value']) 
        bound = compute_bounds(history_data, conf.FRAME_SIZE, conf.MUL_FACTOR)
        if sensor_value > max_limit or sensor_value < min_limit:
            print("Making request to Mailgun to send an email")
            response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(sensor_value))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
        if not bound :
            history_data.append(sensor_value)
            time.sleep(10)
            continue
        elif sensor_value > bound[0] or sensor_value < bound[1]:
            print ("Someone has opened the fridge door.")
        history_data.append(sensor_value);
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)