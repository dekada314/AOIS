class IntConverter:
    def __init__(self, register_size: int = 32):
        self.register_size = register_size
        
    def unsigned_to_binary(self, num: int) -> list[int]:
        num_2 = []
        while num:
            num_2.append(num % 2)
            num //= 2
        num_2 = num_2[::-1]
        num_2 = (self.register_size - len(num_2)) * [0] + num_2
        return num_2
    
    def unsigned_from_binary(self, bin_arr: list[int]) -> int:
        output = 0
        for i in range(self.register_size, 0, -1):
            output += bin_arr[-i] * 2 ** (i-1)
        return output
        


