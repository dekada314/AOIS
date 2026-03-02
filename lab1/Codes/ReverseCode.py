from .DirectCode import DirectCode
from ..Conventers.IntConverter import IntConverter


class ReverseCode(DirectCode):
    def __init__(self):
        pass
    
    def to_reverse_binary(self, number: int, conventer: IntConverter) -> list[int]:
        bit_arr = conventer.unsigned_to_binary(abs(number))
        if number >= 0:
            return bit_arr
        
        dumm_arr = [1] * len(bit_arr)
        for i in range(len(bit_arr)):
            bit_arr[i] ^= dumm_arr[i]
        return bit_arr
    
    def from_reverse_binary(self, bits_arr: list[int], conventer: IntConverter) -> int:
        for i, bin in enumerate(bits_arr):
            bits_arr[i] = int(not bin)
        return conventer.unsigned_from_binary(bits_arr)
        
        
        
# rc = ReverseCode()
# intco = IntConverter()
# output = intco.unsigned_to_binary(13)
# print(output)
# print(rc.to_reverse_binary(-13, obj:=IntConverter()))
# print(rc.from_binary())
