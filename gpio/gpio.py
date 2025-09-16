from periphery import GPIO
import time

Write_Pin = 54
Read_Pin = 55

Write_GPIO = GPIO(Write_Pin, "out")
Read_GPIO = GPIO(Read_Pin, "in")

try:
    while True:
        try:
            Write_GPIO.write(True)
            pin_state = Read_GPIO.read()
            print(f"Pin state: {pin_state}")
            time.sleep(1)

            Write_GPIO.write(False)
            pin_state = Read_GPIO.read()
            print(f"Pin state: {pin_state}")
            time.sleep(1)

        except KeyboardInterrupt:
            Write_GPIO.write(False)
            break

except IOError:
    print("Error")

finally:
    Write_GPIO.close()
    Read_GPIO.close()
