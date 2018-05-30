#!/bin/bash

for f in correct/*.conllu; do
  udapy read.Conllu zone=gold files=$f \
        read.Conllu zone=pred files=incorrect/`basename $f` ignore_sent_id=1 \
        eval.Parsing gold_zone=gold > `basename $f .conllu`.eval.txt
done

