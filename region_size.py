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
    if (maxheap == None and re.search("CommandLine flags",line) != None):
        maxheap = re.search("-XX:MaxHeapSize=[0-9]+", line).group()
        sizepolicy = re.search("-XX:+PrintAdaptiveSizePolicy", line)
        if (sizepolicy == None):
            print("please enable logs with -XX:+PrintAdaptiveSizePolicy")
            exit(0)
        print(f"maxheap: {maxheap}")
        
    if re.search("allocation request:.*source: concurrent humongous allocation", line) is not None:
        total += 1
        req = re.search("allocation request: [0-9]+", line).group()
        allocations.append(int(re.search(r"[0-9]+", req).group()))

print(f"found {total} humongous objects in {log}")


if len(allocations) > 0:
    # humongous allocations occur when the request is >= 1/2 the region size

    mb2 = sum(map(lambda x: x < 1*ONEMB, allocations))
    mb4 = sum(map(lambda x: x < 2*ONEMB, allocations))
    mb8 = sum(map(lambda x: x < 4*ONEMB, allocations))
    mb16 = sum(map(lambda x: x < 8*ONEMB, allocations))
    mb32 = sum(map(lambda x: x < 16*ONEMB, allocations))
    mbMax = sum(map(lambda x: x >= 16*ONEMB, allocations))
    # print(mb2, mb4, mb8, mb16, mb32, mbMax)
    print(f"{(mb2/total):.2%} would not be humongous with a 2mb region size (-XX:G1HeapRegionSize)")
    print(f"{(mb4/total):.2%} would not be humongous with a 4mb region size")
    print(f"{(mb8/total):.2%} would not be humongous with a 8mb region size")
    print(f"{(mb16/total):.2%} would not be humongous with a 16mb region size")
    print(f"{(mb32/total):.2%} would not be humongous with a 32mb region size")
    print(f"{mbMax/total:.2%} would remain humongous with a 32mb region size")


#Total created bytes 	1.88 gb
#Total promoted bytes 	n/a
#Avg creation rate 	4.33 mb/sec
#Avg promotion rate 	n/a

