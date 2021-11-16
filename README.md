# gc_log

This package consists of two separate utilities useful for :

* gc_log_visualizer.py
* regionsize.py

# GC Log Visualizer

This was updated to run under Python 3 from the original at https://github.com/hubspot/gc_log_visualizer

# Region Size

The python script regionsize.py will take a gc.log as input and return the percent of Humongous Objects 
that would fit into various G1RegionSize's (2mb-32mb by powers of 2).

```shell
python regionsize.py <gc.log>
found 858 humongous objects in /tmp/gc.log
0.00% would not be humongous with a 2mb region size (-XX:G1HeapRegionSize)
1.28% would not be humongous with a 4mb region size
5.71% would not be humongous with a 8mb region size
18.07% would not be humongous with a 16mb region size
60.96% would not be humongous with a 32mb region size
39.04% would remain humongous with a 32mb region size
```

# GC Log Preparation

The script has been run on ParallelGC and G1GC logs. There may be some oddities/issues with ParallelGC as profiling it hasn't proven overly useful.

The following gc params are required for full functionality.

`-XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCApplicationStoppedTime -XX:+PrintAdaptiveSizePolicy`
