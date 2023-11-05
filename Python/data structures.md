
# Array
```py

```

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
# stack
stack = []
for digit in num:
    while stack and digit < stack[-1]:    # non-decreasing
        stack.pop()
    stack.append(digit)

```





# Dictionary
```py
# Counter
from collections import Counter

num_counts = Counter(numbers)
unique_numbers = [num for num, count in counts.items() if count == 1]

```
```py
# defaultdict
from collections import defaultdict

```


# Graph

```py
# build
graph = defaultdict(list)
for seq in sequences:
    for f, t in zip(seq, seq[1:]):  
        graph[f].append(t)


```
