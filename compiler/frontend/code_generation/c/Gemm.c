// GEMM OPERATOR $NAME

$DEFINE_CONNECTED_OUTPUT

$TYPE_WEIGHTS weight_$NAME[$OUTPUT_SIZE * $INPUT_SIZE] = {
    $WEIGHTS
};

$TYPE_BIAS bias_$NAME[$OUTPUT_SIZE] = {
    $BIAS
};

#ifdef CONNECTED_OUTPUT
float tensor_$OUTPUT_NAME[$OUTPUT_SIZE * $BATCH_SIZE] = {
    $OUTPUT_INIT
};
#undef CONNECTED_OUTPUT
#endif

for(int b=0; b<$BATCH_SIZE; b++) {
    for(int i=0; i<$OUTPUT_SIZE; i++) {
        float temp = 0.0f;
        for(int j=0; j<$INPUT_SIZE; j++) {
            temp += weight_$NAME[i * $INPUT_SIZE + j] * tensor_$INPUT_NAME[j + b * $BATCH_SIZE];
        }
        tensor_$OUTPUT_NAME[i + b * $BATCH_SIZE] = temp + bias_$NAME[i];
    }
}
