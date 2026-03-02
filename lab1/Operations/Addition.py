from ..Codes.AdditionalСode import AdditionalCode
from ..Conventers.IntConverter import IntConverter


class Addition:
    def __init__(self, register_size: int = 32):
        self.register_size = register_size
    
    def add_additional_codes(self, number1: int, number2: int, int_converter: IntConverter, add_converter: AdditionalCode) -> int:
        bin_number1 = add_converter.to_additional_binary(number1, int_converter)
        bin_number2 = add_converter.to_additional_binary(number2, int_converter)
        
        print(bin_number1)
        print(bin_number2)
        print()
        
        output = [0] * self.register_size
        carry = 0
        for i in range(1, self.register_size + 1):
            curr_sum = bin_number1[-i] + bin_number2[-i] + carry
            match curr_sum:
                case 0:
                    output[-i] = 0
                case 1:
                    output[-i] = 1
                case 2:
                    output[-i] = 0
                    carry = 1
                case 3:
                    output[-i] = 1
                    carry = 1
        return (output, number1 + number2)
        
        
if __name__ == "__main__":
    add = Addition(32)
    bin_output, ox_output = add.add_additional_codes(15, -12, obj1 := IntConverter(), obj2 := AdditionalCode())
    print(bin_output, ox_output, sep='\n')
