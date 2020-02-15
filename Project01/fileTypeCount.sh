#!/bin/bash
echo "Enter the file extension you want to search (without the period):"
read extension
ls *."$extension" | wc -l
