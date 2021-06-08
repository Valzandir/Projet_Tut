#!/bin/bash




ssh_usageDisque(){

	#ip de l'ordinateur distant
	IP_ADDRESS="192.168.1.32"
	#nom d'utilisateur
	USERNAME="yan"
	#port ssh par default
	PORT=22

	

	ssh -t -T -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -l ${USERNAME} ${IP_ADDRESS} -p ${PORT} << "ENDSSH"
	#récuperer l'espace disque et afficher ligne par ligne, sous format standard et lisible par l'homme seulement le nom et puis l'espace.printf a pour parametre les spécifications de format. s = string
	df -Ph | awk '{printf("%10s\t%s\n",$1,$5)}'
ENDSSH

}

chercher_fichiers(){

	#chemin a partir d'ou l'on cherche les fichiers
	SEARCH_PATH="/"
	#formats recherchés
	MULTIMEDIA_EXT="\.mkv$|\.webm$|\.flv$|\.vob$|\.ogg$|\.ogv$|\.drc$|\.gifv$|\.mng$|\.avi$|\.mov$|\.qt$|\.wmv$|\.yuv$|\.rm$|\.rmvb$|/.asf$|\.amv$|\.mp4$|\.m4v$|\.mp4$|\.m?v$|\.svi$|\.3gp$|\.flv$|\.f4v$|\.mp3$"
	
	#trouver tous les fichers dans le chemin precise, filtrer les fichiers multimedia puis on affiche les details
	#si le fichier a un espace dedans,erreur
	# xargs prends en parametre l'output de la commande et le passe en argument pour la commande précisé juste apres. sans ça, on ne peut pas chainer la commande ls directement avec les resultats de la commande
	find "${SEARCH_PATH}/" -type f | grep -E "${MULTIMEDIA_EXT}" | xargs ls -lh

}

multimedia_sauvegarde(){

	#cree un fichier log contenant les details des fichiers multimedia

	#nom du fichier
	LOG_FILE_NAME="log.txt"
	#chemin de la recherche
	SEARCH_PATH="/"
	#formats
	MULTIMEDIA_EXT="\.mkv$|\.webm$|\.flv$|\.vob$|\.ogg$|\.ogv$|\.drc$|\.gifv$|\.mng$|\.avi$|\.mov$|\.qt$|\.wmv$|\.yuv$|\.rm$|\.rmvb$|/.asf$|\.amv$|\.mp4$|\.m4v$|\.mp4$|\.m?v$|\.svi$|\.3gp$|\.flv$|\.f4v$|\.mp3$"
	
	find "${SEARCH_PATH}/" -type f | grep -E ${MULTIMEDIA_EXT} | while read -r line ;
	do 
	
		result="$(echo $line | awk -F "." '{print $NF}') $(ls -l $line | awk '{printf("%10sMB %s\n",$5/1024^2,$9 ) }')"
		echo $result >> ${LOG_FILE_NAME}

	done


}
detecter_grosFichiers(){

	#detecter les gros fichiers multimedia de plus de 50mo

	#definir la taille max des fichiers
	MAXSIZE=50
	SEARCH_PATH="/"
	MULTIMEDIA_EXT="\.mkv$|\.webm$|\.flv$|\.vob$|\.ogg$|\.ogv$|\.drc$|\.gifv$|\.mng$|\.avi$|\.mov$|\.qt$|\.wmv$|\.yuv$|\.rm$|\.rmvb$|/.asf$|\.amv$|\.mp4$|\.m4v$|\.mp4$|\.m?v$|\.svi$|\.3gp$|\.flv$|\.f4v$|\.mp3$"
	find "${SEARCH_PATH}/" -type f | grep -E ${MULTIMEDIA_EXT} | while read -r line ;
	do 
	#vérifier la taille des fichiers
	if [ $(stat -c%s "$line") -gt $(( MAXSIZE *1024*1024 ))  ] ;
	then
		ls -l $line | awk '{printf("%10sMB %s\n",$5/1024^2,$9 ) }'	
		
	fi
	done
	#si on delete, affiche le nom
	read -p "fichier a supprimer: " FILE_PATH
	#chercher fichier
	new_path=$(find "${SEARCH_PATH}/" -type f | grep -i -E ${FILE_PATH})
	#confirmation
	if [[ -f ${new_path} ]]
	then
		
		echo "voulez-vous supprimer ${new_path}?"
		select yn in "Oui" "Non"; do
			case $yn in
				Oui ) echo "supprime ${new_path}";rm ${new_path}; break;;
				Non ) break;;
			esac
		done
	else
		echo "fichier non trouve"
	fi
	
}


#main programme
select task in "Usage disque distant" "detecter les fichiers multimedia" "creer fichier log" "detecter gros fichiers" "quit";do
	case $task in
		"Usage disque distant" ) ssh_usageDisque ; break;;
		"detecter les fichiers multimedia" ) chercher_fichiers ;break;;
		"creer fichier log" ) multimedia_sauvegarde;break;;
		"detecter gros fichiers" ) detecter_grosFichiers;break;;	
		"quit" ) exit;;
	esac
done
