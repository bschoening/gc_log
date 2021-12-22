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

timeUser=[]
timeSys=[]
timeReal=[]

szEden=[]
szSurvivors=[]
szHeap=[]

maxheap=None
units= { 'K' : 1_000, 'M' : 1_000_000, 'G' : 1_000_000_000 }
def parseTimes(line):
    pass

def plotTimes(line):
    pass

def parseGenerations(line):
    """
    Parses an input line from gc.log into a set of tokens and returns them
    """
    generations = re.match(".*Eden:\s(\d+.\d+)(\w).*Survivors:\s(\d+.\d+)(\w).*Heap:\s(\d+.\d+)(\w)", line)
    if generations:
        eden, survivors, heap = round(float(generations.group(1))), round(float(generations.group(3))),
        round(float(generations.group(5)))
        print(eden, survivors, heap)
        return eden*units[generations.group(2)], survivors*units[generations.group(4)], heap**units[generations.group(6)]

def plotGenerations(eden, survivors, heap):
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame.from_dict({"eden" : eden, "survivors" : survivors, "total_heap" : heap})
    fig = px.line(df, x=df.index, y=[df.eden, df.survivors, df.total_heap], title='Generation Size')
    fig.show()

for line in f.read().splitlines():
    if (maxheap == None and re.search("CommandLine flags",line) != None):
        maxheap = re.search("-XX:MaxHeapSize=[0-9]+", line).group()
        concgcthreads = re.search("-XX:ConcGCThreads=[0-9]+", line)
        parallelgcthreads = re.search("-XX:ParallelGCThreads=[0-9]+", line)
        threads = concgcthreads.group() if concgcthreads else parallelgcthreads.group() if parallelgcthreads else None
        sizepolicy = re.search("-XX:\+PrintAdaptiveSizePolicy", line)
        if (sizepolicy == None):
            print("please enable logs with -XX:+PrintAdaptiveSizePolicy")
            exit(0)
        print(f"maxheap: {maxheap}")
        print(f"GC threads: {threads}")
        
    if re.search("allocation request:.*source: concurrent humongous allocation", line) is not None:
        total += 1
        req = re.search("allocation request: [0-9]+", line).group()
        allocations.append(int(re.search(r"[0-9]+", req).group()))

    time = parseTimes(line)
    if time:
        user, sys, real = time
        timeUser.append(user)
        timeSys.append(sys)
        timeReal.append(real)

    generations = parseGenerations(line)
    if generations:
        eden, survivors, heap = generations
        szEden.append(eden)
        szSurvivors.append(survivors)
        szHeap.append(heap)

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
