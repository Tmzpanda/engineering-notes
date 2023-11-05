
# array


```py
# zip
for user, web, time in zip(username, website, timestamp):
    activities.append((user, web, time))

# sort
activities.sort(key=lambda x:x[2])

```

```py
# combinations
from itertools import combinations
patterns = set(combinations(userToWebs[user], 3))

```
```py

```
```py

```





# dictionary
```py
# Counter
from collections import Counter

def find_max_unique(numbers):
    num_counts = Counter(numbers)
    unique_numbers = [num for num, count in counts.items() if count == 1]

    return max(unique_numbers)

```
```py
# defaultdict
from collections import defaultdict

```
