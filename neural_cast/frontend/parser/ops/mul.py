from neural_cast.frontend.parser.node.op_node import OpNode
from neural_cast.frontend.parser.node.node import Node
from neural_cast.frontend.parser.node.output_node import OutputNode
from neural_cast.frontend.parser.node.input_node import InputNode
from neural_cast.frontend.parser.node.init_node import InitializerNode
from neural_cast.frontend.parser.node_types.node_type import NodeType
from neural_cast.frontend.parser.node_types.tensor_type import TensorType
from neural_cast.frontend.common.common import fix_identifier
from neural_cast.frontend.exceptions.CompilerException import CompilerException
import math
from neural_cast.frontend.parser.ops.common.common import node_shape
from neural_cast.frontend.parser.ops.common.common import node_type_binary_operation
from neural_cast.frontend.common.common import onnx_type_to_c_dictionary

class Mul(OpNode):
    def __init__(self, name : str):
        super().__init__(name)

    def __str__(self):
        return super().__str__()

    def generate_code(self) -> str:
        name : str = fix_identifier(self.get_name())
        define_connected_output : str = self._gen_define_connected_output()
        input_name_1 : str = fix_identifier(self._input_varnames[0])
        input_name_2 : str = fix_identifier(self._input_varnames[1])
        output_name : str = fix_identifier(self._output_varnames[0])
        in_shape : int = self.infer_output_shape()
        in_size : int = math.prod(in_shape)
        for_loop_begin : str = self._gen_for_loop_begin(in_shape)
        for_loop_end : str = self._gen_for_loop_end(in_shape)
        index : str = self._gen_for_loop_index(in_shape)
        output_type : int = self.infer_output_type()
        output_type_str : str = onnx_type_to_c_dictionary(output_type)

        code : str = self._read_template_c("Mul.c")

        code = self._expand_pattern(code, "$NAME", name)
        code = self._expand_pattern(code, "$DEFINE_CONNECTED_OUTPUT", define_connected_output)
        code = self._expand_pattern(code, "$INPUT1_NAME", input_name_1)
        code = self._expand_pattern(code, "$INPUT2_NAME", input_name_2)
        code = self._expand_pattern(code, "$OUTPUT_NAME", output_name)
        code = self._expand_pattern(code, "$INPUT_SIZE", str(in_size))
        code = self._expand_pattern(code, "$FOR_LOOPS_BEGIN", for_loop_begin)
        code = self._expand_pattern(code, "$FOR_LOOPS_END", for_loop_end)
        code = self._expand_pattern(code, "$INDEX", index)
        code = self._expand_pattern(code, "$OUTPUT_TYPE", output_type_str)

        return code
    
    def generate_includes_code_c(self) -> str:
        return ""
    
    def generate_declaration_code_c(self) -> str:
        return ""
    
    def infer_output_shape(self) -> list[list[int]]:
        input1 : Node = self._inputs[0]
        shape1 : list[int] = node_shape(input1)

        input2 : Node = self._inputs[1]
        shape2 : list[int] = node_shape(input2)

        if list(shape1) != list(shape2):
            raise CompilerException("Error: inputs in Mul operator must have the same shape")
        
        return shape1
    
    def infer_output_type(self) -> int:
        input1 : Node = self._inputs[0]
        input2 : Node = self._inputs[1]
        return node_type_binary_operation(input1, input2, "mul")

    def get_op_type(self) -> str:
        return "Mul"
    
    def _gen_define_connected_output(self, ) -> str:
        connected_output : bool = isinstance(self._outputs[0], OutputNode)
        
        if connected_output:
            define_connected_output = ""
        else:
            define_connected_output = "#define CONNECTED_OUTPUT"
        
        return define_connected_output

    def _gen_for_loop_begin(self, shape : list[int]) -> str:
        code : str = ""
        n_dims = len(shape)
        for dim in range(n_dims):
            size : int = shape[dim]
            index : str = "i" + str(dim)
            code += "for(" + \
                    "int " + index + "=0; " + index + "<" + str(size) + "; " + index + "++) {\n"
        return code
    
    def _gen_for_loop_end(self, shape : list[int]) -> str:
        code : str = ""
        n_dims = len(shape)
        for _ in range(n_dims):
            code += "}\n"
        return code
    
    def _gen_for_loop_index(self, shape : list[int]) -> str:
        code : str = ""
        n_dims : int = len(shape)
        for i in range(n_dims):
            index : str = "i" + str(i)
            size : int = 1
            for j in range(i+1, n_dims):
                size *= shape[j]
            code += index + "*" + str(size)
            if i < n_dims-1:
                code += " + "
        return code