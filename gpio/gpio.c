#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    int gpio_pin;
    
    printf("Please enter the GPIO pin number: ");
    scanf("%d", &gpio_pin);
    
    FILE *export_file = fopen("/sys/class/gpio/export", "w");
    if (export_file == NULL) {
        perror("Failed to open GPIO export file");
        return -1;
    }
    fprintf(export_file, "%d", gpio_pin);
    fclose(export_file);

    char direction_path[50];
    snprintf(direction_path, sizeof(direction_path), "/sys/class/gpio/gpio%d/direction", gpio_pin);
    FILE *direction_file = fopen(direction_path, "w");
    if (direction_file == NULL) {
        perror("Failed to open GPIO direction file");
        return -1;
    }
    fprintf(direction_file, "out");
    fclose(direction_file);

    char value_path[50];
    char cat_command[100];
    snprintf(value_path, sizeof(value_path), "/sys/class/gpio/gpio%d/value", gpio_pin);
    snprintf(cat_command, sizeof(cat_command), "cat %s", value_path);
    FILE *value_file = fopen(value_path, "w");
    if (value_file == NULL) {
        perror("Failed to open GPIO value file");
        return -1;
    }   

    for (int i = 0; i < 3; i++) {
        fprintf(value_file, "1");
        fflush(value_file);

        system(cat_command);
        sleep(1);

        fprintf(value_file, "0");
        fflush(value_file);
        
        system(cat_command);
        sleep(1);
    }

    fclose(value_file);

    FILE *unexport_file = fopen("/sys/class/gpio/unexport", "w");
    if (unexport_file == NULL) {
        perror("Failed to open GPIO unexport file");
        return -1;
    }
    fprintf(unexport_file, "%d", gpio_pin);
    fclose(unexport_file);

    return 0;
}
