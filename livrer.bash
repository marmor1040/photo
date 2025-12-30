#!/bin/bash

cible="C:/Users/marc/Documents/Developpement logiciels/Officiel/Photo"
echo "tag :"$1
if [ ! -d "$cible" ]
then
  mkdir "$cible"
fi
rm -r "$cible"/src "$cible"/common "$cible"/Ihm "$cible"/FenetreArborescence  "$cible"/FenetreVisionneuse
cp -r common "$cible"
cp -r src "$cible"
cp -r Ihm "$cible"
cp -r FenetreArborescence "$cible"
cp -r FenetreVisionneuse "$cible"
cp -r Data "$cible"
# cp -r Placements "$cible"
cp PhotoSee.py "$cible"
cp PhotoSee.bash "$cible"
if [ "Z$1" != "Z" ]
then
  echo $1 > "$cible/version"
fi
echo "terminé"
sleep 10