class PointerLikeVar:
    def __init__(self, name):
        self.name = name
    
    def Change(self, name):
        self.name = name
    
    # Special method to return self.name when accessed directly
    def __get__(self):
        return self.name
    
    # Special method to compare equality of self.name with another value
    def __eq__(self, other):
        if isinstance(other, PointerLikeVar):
            return self.name == other.name
        return self.name == other
    
    # Special method to calculate the hash based on the name
    def __hash__(self):
        return hash(self.name)

# Example usage
d = {"1": 1, "2": 2}
a = PointerLikeVar("1")
b = a
print(d[a] == d[b])  # Initially, this should be True

a.Change("2")
print(d[a] == d[b])  # After changing `a`'s name, this should be False