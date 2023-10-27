# maximum number that occurs only once in a list 
from collections import Counter

def find_max_unique(numbers):
    num_counts = Counter(numbers)
    unique_numbers = [num for num, count in counts.items() if count == 1]

    return max(unique_numbers)
