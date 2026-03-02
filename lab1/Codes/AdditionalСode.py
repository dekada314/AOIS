from ..Conventers.IntConverter import IntConverter
from .ReverseCode import ReverseCode


class AdditionalCode(ReverseCode):
    def __init__(self):
        pass
    
    def to_additional_binary(self, number: int, conventer: IntConverter) -> list[int]:
        bin_arr = self.to_reverse_binary(number, conventer)
        if bin_arr[0] == 0:
            return bin_arr
        
        
        i = -1
        while abs(i) != len(bin_arr):
            if bin_arr[i] == 0:
                bin_arr[i] = 1
                return bin_arr
            bin_arr[i] = 0
            i -= 1
        return bin_arr
    
if __name__ == "__main__":
    adc = AdditionalCode()
    rvc = ReverseCode()
    # print(rvc.to_reverse_binary(-28, obj := IntConverter()))
    # print(adc.to_additional_binary(-28, obj := IntConverter()))
