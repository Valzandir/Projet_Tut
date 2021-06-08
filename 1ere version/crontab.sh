#!/bin/bash

#NOTE: pour utiliser le scrip faire crontab -e  puis mettre "* * * * * ./funct5.sh" 


#trouve le dossier work et le script est lancé quand trouvé

Spath=$(find "$(pwd -P)" -not -path '*/\.*' -name "work") 

if test $HOME/"Backup" #teste si le dossier backup est ancien
then
  rm -rf $HOME/"Backup" #si version ancienne trouvee,delete
fi

mkdir "Backup" #recrée le fichier backup dans home
Dpath=$HOME/"Backup" #save le backup au chemin de destination 

for f in $(ls $Spath) #une iteration pour chaque fichier dans work
do
  cp -r -T "$Spath"/ "$Dpath" #copie de facon recursive le contenu de work dans backup
done
