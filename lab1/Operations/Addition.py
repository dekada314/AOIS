from ..Codes.AdditionalСode import AdditionalCode
from ..Conventers.IntConverter import IntConverter


class Addition:
    def __init__(self, register_size: int = 32):
        self.register_size = register_size
        
    def _sum(self, bin_arr1: list[int], bin_arr2: list[int]) -> list[int]:
        output = [0] * self.register_size
        carry = 0
        for i in range(1, self.register_size + 1):
            curr_sum = bin_arr1[-i] + bin_arr2[-i] + carry
            match curr_sum:
                case 0:
                    output[-i] = 0
                case 1:
                    output[-i] = 1
                    carry = 0
                case 2:
                    output[-i] = 0
                    carry = 1
                case 3:
                    output[-i] = 1
                    carry = 1
        return output
    
    def add_additional_codes(self, number1: int, number2: int, int_converter: IntConverter, add_converter: AdditionalCode) -> list[int]:
        bin_number1 = add_converter.to_additional_binary(number1, int_converter)
        bin_number2 = add_converter.to_additional_binary(number2, int_converter)
        
        print(bin_number1)
        print(bin_number2)
        print()
        
        return self._sum(bin_number1, bin_number2)
        
        
# if __name__ == "__main__":
    # add = Addition(32)
    # bin_output = add.add_additional_codes(0, -1, obj1 := IntConverter(), obj2 := AdditionalCode())
    # print(bin_output, sep='\n')
    # print(obj2.from_additional_binary(bin_output, obj1))
