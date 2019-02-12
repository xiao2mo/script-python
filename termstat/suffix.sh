# ${line:0:2} this is from left to right
# ${line:2}  this is from left to end
# ${line:0-2} this is from right to left
a=0
awk '{print $1}' $1 > $1.tmp
cat $1.tmp |while read line
do
    echo ${line:0-1}
    let a=a+1 
done
rm $1.tmp
