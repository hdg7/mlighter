#!/bin/bash

count=0
for file in `ls $2/crashes/*`
do
    python3 $1 $file > crash_$count.txt 2> crash_error_$count.txt
    count=$((count + 1))
done
