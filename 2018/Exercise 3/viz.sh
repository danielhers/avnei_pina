#!/bin/bash

for d in correct incorrect; do
  mkdir -p ${d}_tex
  cd ${d}_tex
  for f in ../$d/*.conllu; do
    tex=`basename $f .conllu`.tex
    rm -f $tex
    udapy write.Tikz < $f > $tex
    sed -i 's/\$/\\$/g' $tex || exit 1
    sed -i '2i\\\\pagestyle{empty}' $tex || exit 1
    ~/bin/textogif -png $tex || exit 1
    rm -f $tex
  done
  cd ..
done
for f in correct_tex/*.png; do
  convert $f incorrect_tex/`basename $f` +append `basename $f` || exit 1
done
rm -rf correct_tex incorrect_tex
