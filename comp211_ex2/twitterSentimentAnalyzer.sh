#!/bin/bash

in_file='tweetsmall.txt'
out_file='sentimentpertweet.txt'

# reading input files
readarray positive < positive.txt
readarray negative < negative.txt

# deleting old output file if it already exists
if [ -f $out_file ]; then
   rm sentimentpertweet.txt
fi
 
sentiment=0
line_num=1

# reading tweet input file
while read line; do

    # splitting each tweet into alphabetical-only words
    line_arr=($(echo $line | tr -cs 'a-zA-Z' ' '))

    for i in "${line_arr[@]}"; do
        
        # checking words for positive sentiment
        for j in "${positive[@]}"; do
            if [ $i == $j ]; then
                let sentiment++
            fi
        done
        # checking words for negative sentiment
        for j in "${negative[@]}"; do
            if [ $i == $j ]; then
                let sentiment--
            fi
        done

    done

    # appending positive sentiment to output file
    if [ "$sentiment" -gt "0" ]; then
        echo "Tweet at line #$line_num has a positive sentiment." >> $out_file
    # appending negative sentiment to output file
    elif [ "$sentiment" -lt "0" ]; then
        echo "Tweet at line #$line_num has a negative sentiment." >> $out_file
    # appending neutral sentiment to output file
    elif [ "$sentiment" -eq "0" ]; then
        echo "Tweet at line #$line_num has a neutral sentiment." >> $out_file
    fi

    let "sentiment = 0"
    let line_num++

done < $in_file

exit 0
