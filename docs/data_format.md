# Data Format

Gazeful produces and reads eye-tracked data via `.csv` files in the following
format.
This information is crucial for using already recorded data with Gazeful.

Note that samples of recorded gaze
[can be found here](https://github.com/krznck/gazeful/tree/main/tests/samples).

```csv
#1920x1200
x,y,timestamp
0.2854602783918381,0.15251591056585312,0.0
0.2863858789205551,0.1512339562177658,0.030999999999039574
0.2857642024755478,0.15045832842588425,0.046999999998661224
0.28722967207431793,0.14983608573675156,0.06199999999989814
NA,NA,0.07799999999951979
NA,NA,0.09399999999914144
NA,NA,0.10899999999855936
NA,NA,0.125
0.2894028425216675,0.1486806944012642,0.13999999999941792
0.288333460688591,0.150211863219738,0.15599999999903957
0.28788837790489197,0.1548076942563057,0.17199999999866122
0.28981468081474304,0.15458183735609055,0.18699999999989814
```

The first line should be the resolution of the target screen.
The second line should be the column declaration, `x,y,timestamp`.
Values should be written in floating point format.
When eyes are closed or undetected, the `x` and `y` values should be marked as
`NA`.
