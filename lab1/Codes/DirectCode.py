from ..Conventers.IntConverter import IntConverter


class DirectCode:
    def __init__(self):
        pass
    
    def to_binary(self, number: int, conventer: IntConverter) -> list[int]:
        if number >= 0:
            return conventer.unsigned_to_binary(number)
        
        bits_arr = conventer.unsigned_to_binary(abs(number))
        bits_arr[0] = 1
        return bits_arr
    
    def from_binary(self, bits_arr: list[int], conventer: IntConverter) -> int:
        if bits_arr[0] == 0:
            return conventer.unsigned_from_binary(bits_arr)
        bits_arr[0] = 0
        output = conventer.unsigned_from_binary(bits_arr)
        return -output
        
# directcode = DirectCode()
# print(directcode.to_binary(-123, obj:=IntConverter()))
