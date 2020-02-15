echo "Welcome To My Script!"
echo "Choose one of the following:"
echo "1 for File Size List"
echo "2 for File Type Count"
echo "3 for Find Tag"
read input
if [ "$input" -eq 1 ] ; then
	./fileSizeList.sh
elif [ "$input" -eq 2 ] ; then
	./fileTypeCount.sh
elif [ "$input" -eq 3 ] ; then
	./findTag.sh
else
	echo "Not a Valid Option, Goodbye!"
fi
