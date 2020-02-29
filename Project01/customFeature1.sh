#!/bin/bash
echo "Choose Between the following figures in order to calculate the area: Circle or Square or Rectangle or Triangle"
read figure
if [ "$figure" == "Circle" ]
then
	pi=3.14159
	echo "Enter the radius (in centimenters):"
	read radius
	area=$(echo "scale=2;$pi * $radius * $radius" | bc -l)
	echo "Area of the circle is approximately equal to $area centimeter^2."
elif [ "$figure" == "Square" ]
then
	echo "Enter the length of the side (in centimeters):"
	read side
	area=$(echo "$side^2" | bc -l)
	echo "Area of the sqaure is approximately equal to $area centimeter^2."
elif [ "$figure" == "Rectangle" ]
then
	echo "Enter the length (in centimeters):"
	read length
	echo "Enter the breadth (in centimeters):"
	read breadth
	area=$(echo "$length * $breadth" | bc -l)
	echo "Area of the rectangle is approximately equal to $area centimeter^2."
elif [ "$figure" == "Triangle" ]
then
	echo "Enter the height (in centimeters):"
	read height
	echo "Enter the length of the base (in centimeters):"
	read base
	area=$(echo "0.5 * $height * $base" |  bc -l)
	echo "Area of the triangle is approximately equal to $area centimeter^2."
else
	echo "Invalid Option, Goodbye!"
fi
