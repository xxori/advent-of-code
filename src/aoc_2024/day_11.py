from __future__ import annotations
import math
from functools import lru_cache 

@lru_cache(None)
def recur(n: int, steps: int) -> int:
    # All elements have 1 length if there is no more work
    if steps == 0:
        return 1

    if n == 0:
        return recur(1, steps-1)

    digs = math.floor(math.log10(n)+1)
    if digs % 2 == 0:
        divisor = 10 ** (digs // 2)
        return recur(n//divisor,steps-1) + recur(n%divisor,steps-1)
    
    return recur(n * 2024, steps-1)



if __name__ == '__main__':
    with open("input/2024/11.txt") as f:
        content = f.read()
        nums = [int(x) for x in content.split(" ")]
        r1,r2 = 0,0
        for n in nums:
            r1 += recur(n,25)
            r2 += recur(n,75)
        print("Part 1:",r1)
        print("Part 2:",r2)
        

