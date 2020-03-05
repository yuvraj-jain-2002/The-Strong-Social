#!/bin/bash
echo "Choose an option from the following: Palindrome or Armstrong"
read command
if [ "$command" == "Palindrome" ]
then
	echo "Enter the number:"
	read number
	temp="$number"
	add=0
	i=0
	rem=0
	length=$(echo "${#number}")
	while [ "$i" -lt "$length" ]
	do
		rem=$(( $number % 10 ))
		number=$(( $number / 10 ))
		sub=$(( $add * 10 ))
		add=$(( $sub + $rem ))
		i=$(( "$i" + 1 ))
	done
	if [ "$add" == "$temp" ]
	then
		echo "$add is a palindrome."
	else
		echo "$temp is not a palindrome."
	fi
elif [ "$command" == "Armstrong" ]
then
        echo "Enter a 3-digit number only:"
	read number
	length=$(echo "${#number}")
	if [ "$length" -eq 3 ]
	then
        	temp="$number"
        	add=0
        	i=0
        	rem=0
        	while [ "$i" -lt "$length" ]
        	do
                	rem=$(( $number % 10 ))
                	number=$(( $number / 10 ))
                	sub=$(( $rem * $rem * $rem ))
                	add=$(( $sub + $add ))
                	i=$(( "$i" + 1 ))
        	done
        	if [ "$add" == "$temp" ]
        	then
                	echo "$add is an armstrong number."
        	else
                	echo "$temp is not an armstrong number."
        	fi
	else
		echo "Please enter a 3-digit number."
	fi
else
	echo "Invalid Option, Goodbye!"
fi
