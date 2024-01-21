
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

```py
# queue
from collections import deque

```

```py
# heap
from heapq import heappush, heappop

```

# Set
```py
from functools import reduce
user_with_invites = reduce(set.union, invites.values(), set())
user_without_invites = set(invites.keys()) - user_with_invites

```



# Dictionary
```py
# Counter
from collections import Counter

num_counts = Counter(numbers)
unique_numbers = [num for num, count in num_counts.items() if count == 1]

```
```py
# defaultdict
from collections import defaultdict

graph = defaultdict(list)
for t, f in prerequisites:
    graph[f].append(t)  

```

```py
# OrderedDict

```



```py


```
