#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    printf("Press Ctrl+C to quit\n");
    const char *adc_dir = "/sys/bus/iio/devices/iio:device0";
    char in_voltage0_raw_path[256];
    char in_voltage1_raw_path[256];
    char in_voltage_scale_path[256];

    sprintf(in_voltage0_raw_path, "%s/in_voltage0_raw", adc_dir);
    sprintf(in_voltage1_raw_path, "%s/in_voltage1_raw", adc_dir);
    sprintf(in_voltage_scale_path, "%s/in_voltage_scale", adc_dir);

    FILE *scale_file = fopen(in_voltage_scale_path, "r");
    FILE *in0_raw_file = fopen(in_voltage0_raw_path, "r");
    FILE *in1_raw_file = fopen(in_voltage1_raw_path, "r");

    while (1) {
        char buffer[32];

        fseek(scale_file, 0, SEEK_SET);
        fseek(in0_raw_file, 0, SEEK_SET);
        fseek(in1_raw_file, 0, SEEK_SET);

        if (scale_file && in0_raw_file && in1_raw_file) {
            fgets(buffer, sizeof(buffer), scale_file);
            float scale = strtof(buffer, NULL);

            fgets(buffer, sizeof(buffer), in0_raw_file);
            int in0_raw_value = atoi(buffer);

            fgets(buffer, sizeof(buffer), in1_raw_file);
            int in1_raw_value = atoi(buffer);

            float in0_voltage = (in0_raw_value * scale) / 1000.0;
            float in1_voltage = (in1_raw_value * scale) / 1000.0;

            printf("IN0 Voltage: %.6f V, IN1 Voltage: %.6f V\n", in0_voltage, in1_voltage);
        }
        sleep(1);
    }

    fclose(scale_file);
    fclose(in0_raw_file);
    fclose(in1_raw_file);
    return 0;
}
