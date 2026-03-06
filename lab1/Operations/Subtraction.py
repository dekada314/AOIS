from ..Codes.AdditionalСode import AdditionalCode
from ..Conventers.IntConverter import IntConverter
from .Addition import Addition


class Subtraction(Addition):
    def __init__(self):
        pass
    
    def substract_add_codes(self, num1: int, num2: int, convetner: IntConverter, add_conveter: AdditionalCode) -> list[int]:        
        bin_result = super().add_additional_codes(num1, num2)
        
        if bin_result[0] == 0:
            return bin_result
        return add_conveter.from_additional_binary(bin_result, convetner)
    
    
if __name__ == "__main__":
    add = Addition(32)
    bin_output = add.add_additional_codes(5, -12, obj1 := IntConverter(), obj2 := AdditionalCode())
    print(bin_output, sep='\n')
    print(obj2.from_additional_binary(bin_output, obj1))
