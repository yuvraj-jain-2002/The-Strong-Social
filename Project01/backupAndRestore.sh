#!/bin/bash
echo "Choose one of the following options: Backup or Restore"
read command
if [ "$command" == "Backup" ]
then
	if [ ! -d "./backup" ] ; then
		mkdir backup
	else
		$(find ./backup -type f -delete)
	fi
	files=$(find /home/jainy3/private/CS1XA3/Project01/ -type f -name "*.tmp")
	count=$(find . | grep -i ".tmp" | wc -l)
	if [ "$count" -gt 0 ]
	then
		for file in "$files"
		do
			if [ ! -f "/home/jainy3/private/CS1XA3/Project01/backup/restore.log" ] ; then
				echo "${file}" > '/home/jainy3/private/CS1XA3/Project01/backup/restore.log'
			else
				echo "${file}" >> '/home/jainy3/private/CS1XA3/Project01/backup/restore.log'
			fi
			mv "${file}" ./backup
		done
		echo "Finished"
	else
		echo "There are no .tmp files in the current working direcotry."
	fi
elif [ "$command" == "Restore" ]
then
	echo "Finished"
else
	echo "Invalid Option, Goodbye!"
fi
