# cross
Tool to cross CSV/TSV datasets

## installation

```bash
pip install cross
```

Example:
```bash

Examples:

  - file1:    - file2:
    a,1         b;6
    b,2         d;9
    c,3         k;5
    d,4

      # normal cross (intersection)

      $ cross -f file1 file2 -s ',;' -i 1,1 -os ' '
      b 2 6
      d 4 9

      # union cross

      $ cross -f file1 file2 -s ',;' -i 1,1 -os ',' -u
      a,1,
      k,,5
      c,3,
      b,2,6
      d,4,9

      # symmetric difference cross
      $ cross -f file1 file2 -s ',;' -i 1,1 -os ',' -sd
      a,1,
      k,,5
      c,3,

  - file1:     - file2:      - file3:
    a 1 QW       e 5 QW        99/QQ/z
    b 2 FG       f 6 QW        98/WW/b
    c 3 FG       a 8 FG        97/SS/c
    d 4 YH       a 9 FG
                 a 10 FG
                 a 11 TY
                 b 12 TY

      # union cross with index repetition [-d] 

      $ cross -f file1 file2 file3 -s '  /' -i 1,1,3 -d -u
      a   1   QW  8   FG  9   FG  10  FG  11  TY      
      c   3   FG                                  97  SS
      b   2   FG  12  TY                          98  WW
      e           5   QW                              
      d   4   YH                                      
      f           6   QW                              
      z                                           99  QQ
```
