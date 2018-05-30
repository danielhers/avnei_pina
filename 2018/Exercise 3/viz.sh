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
    ~/bin/textogif -dpi 300 -png $tex || exit 1
    rm -f $tex
  done
  cd ..
done
for f in correct_tex/*.png; do
  convert $f spacer.png incorrect_tex/`basename $f` +append -transparent white -trim `basename $f` || exit 1
done
rm -rf correct_tex incorrect_tex
