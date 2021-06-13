#install bolt iot library first
import conf
from boltiot import Sms, Email, Bolt
import json, time

intermediate_value = 55
max_value = 80


mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)



def twillo_message(message):
  try:
     print("Making request to Twilio to send a SMS")
     response = sms.send_sms(message)
     print("Response received from Twilio is: " + str(response))
     print("Status of SMS at Twilio is :" + str(response.status))
  except Exception as e:
     print("Below are the details")
     print(e)

   
while True:
    print ("Reading Water-Level Value")
    response_1 = mybolt.serialRead('10')
    response = mybolt.analogRead('A0')
    data_1 = json.loads(response_1)
    data = json.loads(response) 
    Water_level = data_1['value'].rstrip()
    print("Water Level value is: " + str(Water_level) + "%")
    sensor_value = int(data['value'])
    temp = (100*sensor_value)/1024
    temp_value = round(temp,2)
    print("Temperature is: " + str(temp_value) + "°C")
    try: 
 
        if int(Water_level) >= intermediate_value:
            message ="Orange Alert!. Water level is increased by " +str(Water_level) + "% in your tank. Please turn off your motor. The current Temperature is " + str(temp_value) + "°C."
            head="Orange Alert"
            twillo_message(message)
            

        if int(Water_level) >= max_value:
           message ="Red Alert!. Water level is increased by " + str(Water_level) + "% in your tank. Please turn off your motor. The Current Temperature is " + str(temp_value) + "°C"
           head="Red Alert!"
           twillo_message(message)
           

    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(15)
