import time

ADC_DIR = "/sys/bus/iio/devices/iio:device0"

def read_value(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

def main():
    print("Press Ctrl+C to quit")
    while True:
        scale_value = float(read_value(f"{ADC_DIR}/in_voltage_scale"))
        IN0_raw_value = float(read_value(f"{ADC_DIR}/in_voltage0_raw"))
        IN1_raw_value = float(read_value(f"{ADC_DIR}/in_voltage1_raw"))

        IN0_voltage = f"{IN0_raw_value * scale_value / 1000:.2f}"
        IN1_voltage = f"{IN1_raw_value * scale_value / 1000:.2f}"

        print(f"IN0_Voltage: {IN0_voltage} V, IN1_Voltage: {IN1_voltage} V")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
