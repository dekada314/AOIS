from src.hash_row import HashRow


class HashTable:
    def __init__(self, size: int = 20):
        self.size = size
        self.rows = [HashRow(i) for i in range(self.size)]
        
    def _calc_hash(self, key_word: str) -> int:
        if len(key_word) < 2:
            key_word += "a" * (2 - len(key_word))
        
        rus_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            
        char1_index = max(rus_alphabet.find(key_word[0].lower()), 0) 
        char2_index = max(rus_alphabet.find(key_word[1].lower()), 0)
        
        return char1_index * 33 + char2_index
        
    def _define_index(self, hash: str) -> int:
        return hash % self.size
    
    def _fill_row(self, index, id, value):
        row: HashRow = self.rows[index]
        row.id = id
        row.c = 0
        row.u = 1
        row.t = 1
        row.l = 0
        row.d = 0
        row.pi = value
        return row
    
    def insert(self, key_word: str, value: str) -> tuple[int, str, str] | None:
        hash_value = self._calc_hash(key_word)
        hash_address = self._define_index(hash_value)
        
        curr_row = self.rows[hash_address]
        if curr_row.u == 0:
            self._fill_row(hash_address, key_word, value)
            return hash_address, key_word, value
        
        if curr_row.id == key_word and curr_row.d == 0:
            return None
        
        initial_address = hash_address
        hash_address = (hash_address + 1) % self.size
        
        while self.rows[hash_address].u != 0 and initial_address != hash_address:
            row = self.rows[hash_address]
            if row.id == key_word and row.d == 0:
                return None
            hash_address = (hash_address + 1) % self.size
        
        if self.rows[hash_address].u == 0:
            inserted_row = self._fill_row(hash_address, key_word, value)
            inserted_row.c = 1
            return hash_address, key_word, value
        
        return None
        
    def search(self, key_word: str) -> tuple[int, str, str] | None:
        hash_value = self._calc_hash(key_word)
        hash_address = initial_address = self._define_index(hash_value)
    
        while self.rows[hash_address].u == 1:
            curr_row = self.rows[hash_address]
            
            if curr_row.id == key_word and curr_row.d == 0:
                return hash_address, key_word, self.rows[hash_address].pi
            
            hash_address = (hash_address + 1) % self.size
            if hash_address == initial_address:
                return None
        return None
    
    def delete(self, key_word: str) -> tuple[int, str, str] | None:
        searched_row = self.search(key_word) 
        if searched_row:
            index, _, value = searched_row
            self.rows[index].d = 1
            return index, key_word, value
        return None
    
    def get_fill_factor(self) -> float:
        filled = sum([1 for row in self.rows if row.u == 1])
        return filled / self.size