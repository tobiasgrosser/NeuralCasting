#include <stdio.h>

#define INPUT_SIZE (4)
#define OUTPUT_SIZE (4)

int main() {
    float input_left[INPUT_SIZE] = {
        0.0f, 1.0f,
        2.0f, 3.0f
    };

    float input_right[INPUT_SIZE] = {
        0.0f, 1.0f,
        2.0f, 3.0f
    };

    float output[OUTPUT_SIZE] = {
        0.0f, 0.0f,
        0.0f, 0.0f
    };

    run_inference(input_left, input_right, output);

    FILE* file;
    file = fopen("test_output.txt", "w");
    for(int i=0; i<OUTPUT_SIZE; i++) {
        fprintf(file, "%f", output[i]);
        if(i < OUTPUT_SIZE-1)
            fprintf(file, " ");
    }
    fclose(file);

    return 0;
}