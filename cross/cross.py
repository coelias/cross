#!/usr/bin/python

from itertools import *
import re
import argparse

class Counter():
    def __init__(self):
        self.data={}

    def update(self,l):
        for i in l:
            if i not in self.data:
                self.data[i]=1
            else:
                self.data[i]+=1

    def __getitem__(self,k):
        if k not in self.data: return 0
        return self.data[k]

HELP='''
cross - Tool to cross TSV/CSV datasets by Carlos del Ojo Elias (deepbit@gmail.com)

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

      \________/ \_____________________________/  \____/
         file1                file2                file3

  - file1:          - file2:
    idx_1,red         22cm,item(55)
    idx_2,brown       34cm,item(22)
    idx_3,blue        55cm,item(3)
    idx_4,yellow      12cm,item(18)
                      43cm,item(1)

      # treating indexes with regular expressions

      $ cross -f file1 file2 -i 1,2 -s',,' -r ';[0-9]+;[0-9]+'
      1      red     43cm
      3      blue    55cm

  - file1:          - file2:

    field1 field2     d 45
    b 12              a 0        
    c 14              z 99
    d 16
      
      # ignoring headers (first line) in first file (-hd '10')

      $ cross -f file1 file2 -i 1,1 -s'  ' -hd '10' -u
      d   16   45
      b   12
      c   14
      a        0
      z        99



CROSS\n\n

'''       
def main():
    parser = argparse.ArgumentParser(description='',usage=HELP)
    
    parser.add_argument("-f", dest="files",help="Files to cross",required=True,nargs='+')
    parser.add_argument("-i", dest="indexes",help="Indexes on the columns to cross for each file (eg: 1,1,2,3)",required=True)
    parser.add_argument("-hd", dest="headers",help="binary list of headers presence per file (eg: 1011) [optional]")
    parser.add_argument("-s", dest="separators",help="Separator used in each file (eg: ',,\t ') First two files use coma, third tab and forth spaces ",required=True)
    parser.add_argument("-os", dest="setarator_output",help="Output separator [\t]",default='\t')
    parser.add_argument("-u", dest="union",help="union of datasets (intersection by default)",action='store_true')
    parser.add_argument("-sd", dest="symmetricdifference",help="symmetric difference of datasets (intersection by default)",action='store_true')
    parser.add_argument("-r", dest="indexregex",help="Regular expression to apply to indexes, specify separator character first and then one regex per field, eg: ';regex1;regex2;regexN'")
    parser.add_argument("-d", dest="duplication",help="allow repeated keys in the same file",action='store_true')
    parser.add_argument("-n", dest="null",help="Specify null value, '' by default",default='')
    options = parser.parse_args()
    
    if options.indexregex:
        regexes = options.indexregex[1:].split(options.indexregex[0])
        regexes = [re.compile(i) for i in regexes]
    else:
        regexes = [None]*len(options.files)
    
    if not options.headers:
        options.headers = '0'*len(options.files)
    
    
    data = {}
    filefounds={}
    totalkeycount = Counter()
    
    seps = options.separators.replace('\\t', '\t')
    idxs = [int(i) for i in options.indexes.split(',')]
    
    if not len(options.files) == len(seps) == len(idxs) == len(options.headers) == len(regexes):
        print ("number of characters in separators must be equal to indexes, input files [, headers] [, and regular expressions]")
        parser.usage()
    
    acum = 0
    file_count=0
    
    for fil, sep, index, headers, regex in izip(options.files, seps, idxs, options.headers, regexes):
        file_count+=1
        headers = int(headers)
        index -= 1
    
        maxwidth = 0
    
        filekeycount = {}
    
        for line in open(fil):
            if headers:
                headers -= 1
                continue
    
            line = line.strip().split(sep)
            try: 
                key = line.pop(index)
                if regex:
                    key = regex.findall(key)[0]
                assert key
            except:
                continue
    
            if not options.duplication:
                filekeycount.setdefault(key, 0)
                filekeycount[key] += 1
                if filekeycount[key] > 1:
                    raise Exception('key {} appears more than once in {}, duplication not enabled [-d]!'.format(key, fil))
    
            if key not in data:
                data[key] = []
            if key not in filefounds:
                filefounds[key]=set()
    
            row = data[key]
            filefounds[key].add(file_count)
    
            totalkeycount.update([key])
    
            if len(row) < acum:
                row.extend([options.null]*(acum-len(row)))
    
            row.extend(line)
    
            newlength = len(row)-acum
            if newlength > maxwidth:
                maxwidth = newlength
    
    
        acum += maxwidth
    
    if options.union:
        for i, row in data.iteritems():
            if len(row) < acum:
                row.extend([options.null]*(acum-len(row)))
            print (options.setarator_output.join([i]+row))
    elif options.symmetricdifference:
        for i, row in data.iteritems():
            if totalkeycount[i] == 1:
                row.extend([options.null]*(acum-len(row)))
                print (options.setarator_output.join([i]+row))
    else:
        for i, row in data.iteritems():
            if len(filefounds[i]) == len(options.files):
                if len(row) < acum:
                    row.extend([options.null]*(acum-len(row)))
                print (options.setarator_output.join([i]+row))
    
