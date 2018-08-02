#!/bin/sh
# dict/all.dict 为一个大词典，最好把目前已有的所有分类的词典都放进去,
# 输入两个文件的格式，统一为 term \t tag
# 输出文件的格式: term \t tag(in $1) \t tags in all.dict
# 示例: sh script/build_ambiguity_dict.sh dict_raw/lit.book.dict > tmp/lit.book.ambiguity.dict

awk -F'\t' 'NR==FNR {if($1 in a) {a[$1] = a[$1]"\t"$2;} else {a[$1] = $2;} } NR>FNR {if ($1 in a) {print $0"\t"a[$1];} else {print $0;} }' dict/all.dict $1 
