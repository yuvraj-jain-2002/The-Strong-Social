#!/bin/bash
echo "Enter the tag (a single word):"
read tag
if [ ! -f "$tag".log ] ; then
	touch "$tag".log
else
	rm "$tag".log
	touch "$tag".log
fi
pythonFile=`find . -type f -name "*.py" | wc -w`
if [ "$pythonFile" -gt 0 ] ; then
	cat *.py | grep ^# | grep "$tag" >> "$tag".log
fi
