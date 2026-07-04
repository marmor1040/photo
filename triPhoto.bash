#!/bin/bash

echo $0
chemin=$(echo $0 | sed s/\ /_/g)
rep=$(dirname $chemin)
location=$(basename $rep)
echo "Exécution triPhoto"
off=$(echo $rep | grep Officiel)
if [ $? = 0 ]
then
  echo "Officiel"
  export REP_EXE="C:/Users/Marc/Documents/Developpement logiciels/Officiel/Photo"
else
  echo "dev"
  export REP_EXE="C:/Users/Marc/Documents/Developpement logiciels/Spyder3/Photo"
fi
export PYTHONPATH="$REP_EXE/src":$PYTHONPATH
python "$REP_EXE/triPhoto.py"
echo "sleep 10 sec ..."
sleep 10