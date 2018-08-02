#!/bin/sh
awk -F'\t' 'NR==FNR {
   a[$1] = a[$1] "\t" $2;
}
NR>FNR {
   if ($1 in a) {
       print $0"\t"a[$1];
   } else {
       print $0;
   }
}' $1 $2
