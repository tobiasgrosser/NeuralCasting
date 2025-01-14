import torch
import neural_cast as cmp
from neural_cast.compiler import run
from neural_cast.frontend.common.common import CompilerConfig
import subprocess
import unittest
import onnxruntime as ort
import numpy as np
import os
import yaml

class TestReimplementedGRU(unittest.TestCase):
    def test_00(self):
        # init config file
        name : str = CompilerConfig()['name']
        output_path : str = CompilerConfig()['output_path']
        test_path : str = CompilerConfig()['test_path']

        # inference onnxruntime
        test_path : str = test_path + 'neural_networks/reimplemented_gru/'
        path_onnx = test_path + 'gru_reimplemented.onnx'
        session = ort.InferenceSession(path_onnx)
        input_name_1 = session.get_inputs()[0].name
        input_name_2 = session.get_inputs()[1].name
        input_data =  np.ones((1, 3), dtype=np.float32)
        hidden_data =  np.zeros((1, 4), dtype=np.float32)
        outputs = session.run(None, {input_name_1: input_data, input_name_2: hidden_data})
        output_onnx = outputs[0]
        output_onnx = np.squeeze(output_onnx)
        output_onnx = output_onnx.flatten()

        # run compiler
        run(CompilerConfig(), framework='onnx', path=path_onnx)

        # read main.c code and add include to nn
        f = open(test_path + 'main.c', 'r')
        main_code : str = "#include \"" + name + ".h\"\n"
        main_code += f.read()
        f.close()

        # generate main.c in output directory
        f = open(output_path + 'main.c', 'w')
        f.write(main_code)
        f.close()
        
        # run command
        try:
            subprocess.run(["bash", test_path + "build.sh", name, output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        # read c output
        f = open(output_path + "test_output.txt")
        output_text : str = f.read()
        f.close()
        output_values_str : list[str] = output_text.split(" ")
        output_c : list[float] = []
        for i in range(len(output_values_str)):
            output_c.append(float(output_values_str[i]))

        print(output_onnx)
        print(output_c)
        # compare results
        self.assertEqual(len(output_onnx), len(output_c))

        N : int = len(output_onnx)
        for i in range(N):
            self.assertAlmostEqual(output_onnx[i], output_c[i], delta=1e-6)
    
    def test_01(self):
        # init config file
        name : str = CompilerConfig()['name']
        output_path : str = CompilerConfig()['output_path']
        test_path : str = CompilerConfig()['test_path']

        # inference onnxruntime
        test_path : str = test_path + 'neural_networks/reimplemented_gru/'
        path_onnx = test_path + 'gru_reimplemented_1.onnx'
        session = ort.InferenceSession(path_onnx)
        input_name_1 = session.get_inputs()[0].name
        input_name_2 = session.get_inputs()[1].name
        input_data =  np.ones((1, 3), dtype=np.float32)
        hidden_data =  np.zeros((1, 4), dtype=np.float32)
        outputs = session.run(None, {input_name_1: input_data, input_name_2: hidden_data})
        output_onnx = outputs[0]
        output_onnx = np.squeeze(output_onnx)
        output_onnx = output_onnx.flatten()

        # run compiler
        run(CompilerConfig(), framework='onnx', path=path_onnx)

        # read main.c code and add include to nn
        f = open(test_path + 'main.c', 'r')
        main_code : str = "#include \"" + name + ".h\"\n"
        main_code += f.read()
        f.close()

        # generate main.c in output directory
        f = open(output_path + 'main.c', 'w')
        f.write(main_code)
        f.close()
        
        # run command
        try:
            subprocess.run(["bash", test_path + "build.sh", name, output_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        # read c output
        f = open(output_path + "test_output.txt")
        output_text : str = f.read()
        f.close()
        output_values_str : list[str] = output_text.split(" ")
        output_c : list[float] = []
        for i in range(len(output_values_str)):
            output_c.append(float(output_values_str[i]))

        print(output_onnx)
        print(output_c)
        # compare results
        self.assertEqual(len(output_onnx), len(output_c))

        N : int = len(output_onnx)
        for i in range(N):
            self.assertAlmostEqual(output_onnx[i], output_c[i], delta=1e-6)

def run_tests():
    curr_file = os.path.abspath(__file__)
    curr_path = os.path.dirname(curr_file)
    with open(curr_path + '/../../../config/config.yaml', 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
    CompilerConfig(config)
    unittest.main()

if __name__ == "__main__":
    run_tests()