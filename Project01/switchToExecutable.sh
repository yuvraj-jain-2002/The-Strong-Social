#!/bin/bash
if [[ ! -e permissions.log ]]; then
	touch permissions.log
fi
echo "Please select one option from the following: Change or Restore"
read command
if [ "$command" == "Change" ] ; then
	if [ $(find . | grep -i ".sh$" | wc -l) -gt 0 ] ; then
		for file in $(find . -type f -name "*.sh")
		do
			if [ -w "${file}" ]
			then
				echo $(ls -l "${file}") > '/home/jainy3/private/CS1XA3/Project01/permissions.log'
				chmod a+w+x "${file}"
				echo "Finished"
			else
				if [ -x "${file}" ]
				then
					echo $(ls -l "${file}") > '/home/jainy3/private/CS1XA3/Project01/permissions.log'
					chmod a-x "${file}"
					echo "Finished"
				fi
			fi
		done
	else
		echo "There are no files with .sh extension"
	fi
elif [ "$command" == "Restore" ] ; then
	permfiles=$(find . -name "permissions.log")
	for final in $("$permfiles" | cut -d'.' -f 2-)
	do
		for iteration in $(stat -c %a "${final}")
		do
			chmod "${iteration}" "${final}"
		done
	done
fi
