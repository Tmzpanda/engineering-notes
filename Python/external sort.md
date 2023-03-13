```

# external sort

time complexity
1. external sort - heap O(k.mlogm + nlogk)
2. topK - heap O(nlogK)
3. merge k sorted list - recursion O(nlogk)
4. merge sort - recursion O(nlogn)


optimization
external sort - heap O(k.mlogm + nlogk)
1. I/O bounded - buffer
2. multiple cores - distribute O(k.mlogm)
3. multiple machines - distribute O(nlogk)
  single machine O(800log8)
  multi machines O([200log2] + 200log2 + 200log2 + 200log2 +
                   [400log2] + 400log2 +
                   [800log2])


heap operation
push - siftup O(logn)
pop - siftdown O(logn)
```
