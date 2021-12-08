//usr/bin/env jshell --show-version --execution local '-J-Xlog:gc+ergo*=trace:/tmp/gc.log' "$0" "$@"; exit $?

/*
  usage:  jshell '-J-Xlog:gc*=debug:/tmp/gc.log:tags,uptime' --execution local GCAllocationTest.jsh
*/

import java.util.stream.IntStream; 
import java.util.Random;

int MB = 1024 * 1024;

IntStream.range(0, 30000).forEachOrdered(n -> {
    if (n % 1000 == 0) { System.out.println(n); };
	java.util.Random random = new java.util.Random();
	int size = MB * (1 + random.nextInt(20));
    byte[] a1 = new byte[size];
    a1[1] = 1;
});

/exit
