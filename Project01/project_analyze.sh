echo "Welcome To My Script!"
echo "Choose one of the following:"
echo "1 for File Size List"
echo "2 for File Type Count"
echo "3 for Find Tag"
echo "4 for Custom Feature 1: Geometric Area Calculation of 2-D figures"
echo "5 for Custom Feature 2: Palindrome and Armstrong"
read input
if [ "$input" -eq 1 ] ; then
	./fileSizeList.sh
elif [ "$input" -eq 2 ] ; then
	./fileTypeCount.sh
elif [ "$input" -eq 3 ] ; then
	./findTag.sh
elif [ "$input" -eq 4 ] ; then
	./customFeature1.sh
elif [ "$input" -eq 5 ] ; then
        ./customFeature2.sh
else
	echo "Invalid Option, Goodbye!"
fi
