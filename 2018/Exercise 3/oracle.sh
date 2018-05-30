#!/bin/bash

for f in correct/*.conllu; do
  awk -v OFS='\t' -F '\t' '{$9=$10=""}1' $f > ${f%u}
  sed -i '/^#/d;s/^\s\+$//' ${f%u}
  java -jar ParseOracleArcStd.jar -t -1 -l 1 -c ${f%u} | grep -v '^\[' > ${f%.*}.oracle.txt
  rm -f ${f%u}
done
rm -f svm_train.svm svm_test.svm output.txt
