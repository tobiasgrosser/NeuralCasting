import torch
import neural_cast as cmp
from neural_cast.compiler import run
from neural_cast.frontend.common.common import CompilerConfig
import subprocess
import unittest
import onnxruntime as ort
import numpy as np
import json
import os
import yaml

class TestGather(unittest.TestCase):
    def test_00(self):
        # init config file
        name : str = CompilerConfig()['name']
        output_path : str = CompilerConfig()['output_path']
        test_path : str = CompilerConfig()['test_path']

        # inference onnxruntime
        test_path : str = test_path + 'neural_networks/gather/'
        path_onnx = test_path + 'gather_axis1.onnx'
        session = ort.InferenceSession(path_onnx)
        input_name_1 = session.get_inputs()[0].name
        input_name_2 = session.get_inputs()[1].name
        values =  np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12]
        ], dtype=np.float32)
        indices = np.array([
            [0, 2],
            [0, 2],
            [0, 2],
        ], dtype=np.int64)
        outputs = session.run(None, {input_name_1: values, input_name_2: indices})
        output_onnx = outputs[0]
        output_shape_onnx = output_onnx.shape
        output_onnx = np.squeeze(output_onnx)
        output_onnx = output_onnx.flatten()

        # run compiler
        run(CompilerConfig(), framework='onnx', path=path_onnx)

        # read inferred output shape
        output_shape_path : str = CompilerConfig()['temp_path'] + "out_shape.json"
        with open(output_shape_path, 'r') as json_file:
            data = json.load(json_file)
            output_keys = list(data.keys())
        output_shape_c = data[output_keys[0]]

        # compare shape
        print("Output shape onnx: ", output_shape_onnx)
        print("Output shape C: ", output_shape_c)
        self.assertEqual(len(output_shape_onnx), len(output_shape_c))
        for i in range(len(output_shape_onnx)):
            self.assertEquals(output_shape_onnx[i], output_shape_c[i])

        # read main.c code and add include to nn
        f = open(test_path + 'main_axis1.c', 'r')
        main_code : str = "#include \"" + name + ".h\"\n"
        main_code += f.read()
        f.close()

        # generate main.c in output directory
        f = open(output_path + 'main_axis1.c', 'w')
        f.write(main_code)
        f.close()
        
        # run command
        try:
            subprocess.run(["bash", test_path + "build_axis1.sh", name, output_path], check=True)
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
        test_path : str = test_path + 'neural_networks/gather/'
        path_onnx = test_path + 'gather_axis0.onnx'
        session = ort.InferenceSession(path_onnx)
        input_name_1 = session.get_inputs()[0].name
        input_name_2 = session.get_inputs()[1].name
        values =  np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12]
        ], dtype=np.float32)
        indices = np.array([
            [0, 2],
            [0, 2],
            [0, 2],
        ], dtype=np.int64)
        outputs = session.run(None, {input_name_1: values, input_name_2: indices})
        output_onnx = outputs[0]
        output_shape_onnx = output_onnx.shape
        output_onnx = np.squeeze(output_onnx)
        output_onnx = output_onnx.flatten()

        # run compiler
        run(CompilerConfig(), framework='onnx', path=path_onnx)

        # read inferred output shape
        output_shape_path : str = CompilerConfig()['temp_path'] + "out_shape.json"
        with open(output_shape_path, 'r') as json_file:
            data = json.load(json_file)
            output_keys = list(data.keys())
        output_shape_c = data[output_keys[0]]

        # compare shape
        print("Output shape onnx: ", output_shape_onnx)
        print("Output shape C: ", output_shape_c)
        self.assertEqual(len(output_shape_onnx), len(output_shape_c))
        for i in range(len(output_shape_onnx)):
            self.assertEquals(output_shape_onnx[i], output_shape_c[i])

        # read main.c code and add include to nn
        f = open(test_path + 'main_axis0.c', 'r')
        main_code : str = "#include \"" + name + ".h\"\n"
        main_code += f.read()
        f.close()

        # generate main.c in output directory
        f = open(output_path + 'main_axis0.c', 'w')
        f.write(main_code)
        f.close()
        
        # run command
        try:
            subprocess.run(["bash", test_path + "build_axis0.sh", name, output_path], check=True)
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