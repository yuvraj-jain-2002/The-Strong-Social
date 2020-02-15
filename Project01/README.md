# COMPSCI 1XA3 Project01

##Introduction:
The projects primarily aim is to make us familiar and more equipped with scripting languages like bash. To execute the project, one need to run the "project_analyze.sh" file, the script displays three options one can select from: File Size List, File Type Count, Find Tag.

##Feature 1 : File Size List
Description: This feature lists all the files which are in the repository, displays their size in data storage units like KB, MB, GB, etc. and also arranges the displayed file in decreasing order based on their storage.
Execution: One can execute this feature by running the "project_analyze.sh" file and then typing 1or by simply running the "fileSizeList.sh" file.
Arguments: This feature does not need any arguments.
Refrence: TA's and [Stack Overflow](https://stackoverflow.com/)

##Feature 2 : File Type Count
Description: This feature returns the number of files which have the following extension inputted by the user in your current working directory.
Execution: One can execute this feature by running the "project_analyze.sh" file and then typing 2 or by simply running the "fileTypeCount.sh" file.
Arguments: The user has to input an extension like .pdf, .png, .sh, .txt, etc. (NOTE: While inputting the extension, the user must omit the period)
Refrence: [2DAYGEEK- This website is a Linux Practice Guide](https://www.2daygeek.com/how-to-count-files-by-extension-in-linux/) 

##Feature 3 : Find Tag
Description: This feature asks the user to input a tag (a single word) and then the system makes a ".log" file of it, if the "tag.log" file already exists, it overwrites it. After that, the system looks for all python files having the lines which begins with a comment (i.e. #) and including the Tag and then copies the lines to ".log" file it created. 
Execution: One can execute this feature by running the "project_analyze.sh" file and then typing 3 or by simply running the "findTag.sh" file.
Arguments: A single word
Refrence: TA's and Lecture Sildes

##Custom Feature 1 : Geometric Area Calculation of 2-D figures
Description: This feature calculates the area of a 2-D figure (mainly circles, squares, rectangles and triangles). The user first chooses between the 2-D figures for which he/she wants to find the area of, and then the user is asked to enter the dimensions of the respective 2-D figure he/she choose.

##Custom Feature 2 : Palindrome and Armstrong
Description: This feature checks whether the inputted number by the user is a palindromic number or an armstrong number, as chosen by the user respectively. (NOTE: A palindromic number is a number that remains the same when its digits are reversed. Whereas, an armstrong number is a number that is equal to the sum of cubes of its digits.)
