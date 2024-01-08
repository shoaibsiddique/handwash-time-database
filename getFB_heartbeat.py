# This code takes the commands to enable/disable a PWM LED connected
# to the RPI Zero W V1.1 at pin 18.
# On enabling the LED Fades In and Out 
# On disabling the LED is OFF.
# The code connectes to the database FB and takes the commands from there.

import RPi.GPIO as GPIO
import asyncio
import time
import firebase_admin
from firebase_admin import credentials, db

LED_PIN = 18
FADE_TIME = 20  # in seconds
PWM_FREQUENCY = 500  # Hz

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

def destroy():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()

def initialize_firebase_app(JSON_DB_File="db-cred.json",
                            ProjectID="handwash-detection-db-001",
                            databaseURL="handwash-detection-db-001.firebaseapp.com"):
    cred = credentials.Certificate(JSON_DB_File)
    Config = {
        "apiKey": "AIzaSyCqZaOX3s6zIeCwv_r73_7EX_aBCDzAxno",
        "authDomain": "handwash-detection-db-001.firebaseapp.com",
        "databaseURL": "https://handwash-detection-db-001-default-rtdb.firebaseio.com",
        "projectId": "handwash-detection-db-001",
        "storageBucket": "handwash-detection-db-001.appspot.com",
        "messagingSenderId": "857179695665",
        "appId": "1:857179695665:web:1435b9041fc8df3555c310",
        "measurementId": "G-R2S4KD4YNV"
    }

    firebase_admin.initialize_app(cred, Config)

def get_data_from_firebase():
    ref = db.reference("/")
    data = ref.get()
    return data

async def fade_in_out_async():
    pwm = None
    try:
        while True:
            val = get_data_from_firebase()["LED_VAL"]
            print(f"The value of state is: {val}")
            
            if val == 1:
                if pwm is None:
                    pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
                    pwm.start(0)
                    print("PWM started")
                
                for duty_cycle in range(0, 101, 5):
                    pwm.ChangeDutyCycle(duty_cycle)
                    await asyncio.sleep(0.1)

                await asyncio.sleep(0.2)  # Pause at full brightness

                for duty_cycle in range(100, -1, -5):
                    pwm.ChangeDutyCycle(duty_cycle)
                    await asyncio.sleep(0.1)

                await asyncio.sleep(0.2)  # Pause at off state
            elif pwm is not None:
                print("PWM stopped")
                pwm.stop()
                pwm = None
                await asyncio.sleep(1)

            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass

    if pwm is not None:
        print("PWM stopped")
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        initialize_firebase_app()
        setup()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(fade_in_out_async())

    except KeyboardInterrupt:
        pass
    finally:
        destroy()
