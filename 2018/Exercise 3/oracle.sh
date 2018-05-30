#!/bin/bash

for f in correct/*.conllu; do
  out=`basename $f .conllu`.oracle.txt
  sed -n '/^# text/{s/# text = //;p}' $f > $out
  awk -v OFS='\t' -F '\t' '{$9=$10=""}1' $f > ${f%u}
  sed -i '/^#/d;s/^\s\+$//' ${f%u}
  java -jar ParseOracleArcStd.jar -t -1 -l 1 -c ${f%u} | grep -v '^\[' >> $out
  rm -f ${f%u}
done
rm -f svm_train.svm svm_test.svm output.txt
