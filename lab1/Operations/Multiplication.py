from ..Codes.DirectCode import DirectCode
from ..Conventers.IntConverter import IntConverter
from .Addition import Addition


class Multiplication:
    def __init__(self, register_size: int = 32):
        self.register_size = register_size
    
    def multiplication(self, num1: list[int], num2: list[int], conventer_to_dir_code: DirectCode, add_opperator: Addition, int_conv: IntConverter) -> list[int]:
        bin_num1 = conventer_to_dir_code.to_binary(num1, int_conv)
        bin_num2 = conventer_to_dir_code.to_binary(num2, int_conv)
        
        print(bin_num1)
        print(bin_num2)
        
        print()
        
        output = [0] * self.register_size
        
        for i in range(-1, -self.register_size, -1):
            sum_arr = bin_num1 if bin_num2[i] == 1 else [0] * self.register_size
            bias = abs(i) - 1
            sum_arr = (sum_arr + [0] * bias)[bias:]
            print(sum_arr)
            output = add_opperator._sum(output, sum_arr)
        
        output[0] = 1 if (num1 < 0 or num2 < 0) else 0
        return output
    
if __name__ == "__main__":  
    add = Addition(32)
    dir = DirectCode()
    mult = Multiplication(32)
    inti = IntConverter()
    bin_output = mult.multiplication(12, -5, dir, add, obj:=IntConverter())
    print(bin_output, sep='\n')
    print(dir.from_binary(bin_output, inti), sep='\n')