from ..Conventers.IntConverter import IntConverter
from .ReverseCode import ReverseCode


class AdditionalCode(ReverseCode):
    def __init__(self):
        pass
    
    def _plus_one(self, bin_arr: list[int]) -> list[int]:
        i = -1
        while abs(i) != len(bin_arr):
            if bin_arr[i] == 0:
                bin_arr[i] = 1
                return bin_arr
            bin_arr[i] = 0
            i -= 1
        return bin_arr
    
    def to_additional_binary(self, number: int, conventer: IntConverter) -> list[int]:
        bin_arr = self.to_reverse_binary(number, conventer)
        if bin_arr[0] == 0:
            return bin_arr
        return self._plus_one(bin_arr)
    
    def from_additional_binary(self, bin_arr: list[int], conventer: IntConverter) -> int:
        if bin_arr[0] == 0:
            return conventer.unsigned_from_binary(bin_arr)
        result = super()._flip_bits(bin_arr)
        result_with_one = self._plus_one(result)
        return -conventer.unsigned_from_binary(result_with_one)
        
    
# if __name__ == "__main__":
    # adc = AdditionalCode()
    # rvc = ReverseCode()
    # print(rvc.to_reverse_binary(-22, obj := IntConverter()))
    # print(rvc.to_reverse_binary(22, obj := IntConverter()))
    # print(adc.to_additional_binary(-22, obj := IntConverter()))
