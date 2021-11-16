import re
import sys


ONEMB = 1_048_576

if len(sys.argv) != 2:
    print("usage: python regionsize.py <gc_log>")
    exit()

log = sys.argv[1]
f = open(log)
allocations = []
total = 0

for line in f.read().splitlines():
    if re.search("allocation request:.*source concurrent humongous allocation", line) is not None:
        total += 1
        req = re.search("allocation request: [0-9]+", line).group()
        allocations.append(int(re.search(r"[0-9]+", req).group()))

print(f"found {total} humongous objects in {log}")

# humongous allocations occur when the request is >= 1/2 the region size

mb2 = sum(map(lambda x: x < 1*ONEMB), allocations)
mb4 = sum(map(lambda x: x < 2*ONEMB), allocations)
mb8 = sum(map(lambda x: x < 4*ONEMB), allocations)
mb16 = sum(map(lambda x: x < 8*ONEMB), allocations)
mb32 = sum(map(lambda x: x < 16*ONEMB), allocations)
mbMax = sum(map(lambda x: x >= 16*ONEMB), allocations)

print(f"{100*mb2/total}% would not be humongous with a 2mb region size (-XX:G1HeapRegionSize)")
print(f"{100*mb2/total}% would not be humongous with a 4mb region size")
print(f"{100*mb2/total}% would not be humongous with a 8mb region size")
print(f"{100*mb2/total}% would not be humongous with a 16mb region size")
print(f"{100*mb2/total}% would not be humongous with a 32mb region size")
print(f"{100*mb2/total}% would remain humongous with a 32mb region size")