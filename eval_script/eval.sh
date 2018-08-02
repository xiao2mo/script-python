#!/bin/sh
#bin/onestepMachineLabel tmp/eval/
#func:convert the raw data with labelto ctf-style (3 colums)
#if [ 0 = 1 ]; then

bin_path=./bin/
truth_file=/home/fanyange/svn/phone_project/ner_data/comp/truth_0908.txt
res_dir=/home/fanyange/svn/phone_project/ner_data/comp/

current_date=`date +%Y%m%d`
no_label_file=$res_dir"/truth_raw."$current_date
truth_crf_file=$res_dir"/truth.crf."$current_date
predict_file=$res_dir"/predict."$current_date
predict_crf_file=$res_dir"/predict.crf."$current_date
truth_vs_predict_file=$res_dir"/truth_vs_predict.crf."$current_date
res_file=$res_dir"/summary."$current_date


python recovery_old.py $truth_file $no_label_file
echo "recovery_old success"

$bin_path"/onestepMachineLabel" $no_label_file  $predict_file
echo "predict success"

$bin_path"/docConll" $truth_file $truth_crf_file ner 3 2 0
$bin_path"/docConll" $predict_file $predict_crf_file ner 3 2 0
echo "docConll success"
#func:paste two file to one(3 colums)
#paste $truth_crf_file $predict_crf_file | awk -F ' ' '{if (NF > 2) {print $1,$4,$NF} else {print $0="\n"} }' > tmp/eval/truth_vs_predict_new.crf

#func:exclude the different colums
python crf_align.py $truth_crf_file $predict_crf_file > $truth_vs_predict_file
echo "crf_align success"
#paste -d " " tmp/eval/truth.crf tmp/eval/predict.old.crf | awk -F ' ' '{print $1,$4,$NF}'  > tmp/eval/truth_vs_predict_old.crf
#paste -d " " tmp/eval/truth.crf tmp/eval/predict.new.crf | awk -F ' ' '{print $1,$4,$NF}'  > tmp/eval/truth_vs_predict_new.crf
#fi
#func:evaluate the  current model on given test data
#python  conlleval.py < tmp/eval/truth_vs_predict_old.crf > tmp/eval/truth_vs_predict_old.summary
python  conlleval.py < $truth_vs_predict_file > $res_file
echo "success"
