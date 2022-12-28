#!/bin/bash

# a function checking if user input is within file bounds
function checkIfWithinBounds()
{
   if [ $1 -gt ${#data[@]} ] || [ $1 -le "0" ]; then
      printf "Error... Input is out of file bounds.\n\n"
      return 1
   fi
}

# a function checking if user input is a valid integer
function checkIfInt()
{
   if expr "$1" : '^[0-9]*$' >/dev/null; then
      return 0
   else
      printf "Error... Input is not a valid integer.\n\n"
      return 1
   fi
}

# a function for printing the menu
function printMenu()
{
    printf "Welcome to a simple Twitter Viewer and Editor!\n"
    printf "\n"
    printf "Below is a list of options that can be performed based on your input:\n"
    printf "' c ' creates a tweet\n"
    printf "' d ' deletes a tweet\n"
    printf "' r ' reads a tweet\n"
    printf "' u ' updates a tweet\n"
    printf "' $ ' reads the last tweet on file\n"
    printf "' - ' reads the previous tweet\n"
    printf "' + ' reads the next tweet\n"
    printf "' = ' prints current tweet\n"
    printf "' q ' close the application\n"
    printf "' w ' (over) write file to secondary storage memory(disk)\n"
    printf "' x ' save changes to the local file and close the application\n"
    printf "\n"
    printf "Type an option: "
}

# a function for " c " option
function optionCreate()
{  
    printf "Type the tweet you want to create: "
    read userText
    data[${#data[@]}]=$userText
    CurTweetID=${#data[@]}     
}

# a function for " d " option
function optionDelete()
{
    userChoice=$1
    data=( "${data[@]:0:$userChoice-1}" "${data[@]:$userChoice}" )
    let "CurTweetID = $userChoice - 1"
}

# a function for " r " option
function optionRead()
{   
    userChoice=$1
    readTweet=${data[$userChoice - 1]}
    printf "The tweet at line #$userChoice is:\n\t$readTweet\n"
    CurTweetID=$userChoice
}

# a function for " u " option
function optionUpdate()
{
    userChoice=$1
    printf "Type the tweet you want as update: "
    read userText
    data[$userChoice-1]=$userText
    CurTweetID=$userChoice
}

# a function for " $ " option
function optionReadLast()
{
    CurTweetID=${#data[@]} 
    printf "The tweet at the last line is:\n\t${data[CurTweetID - 1]}\n"
}

# a function for " - " option
function optionReadPrevious()
{
    let CurTweetID--
    printf "The tweet at the previous line is:\n\t${data[CurTweetID - 1]}\n"
}

# a function for " + " option
function optionReadNext()
{
    let CurTweetID++
    printf "The tweet at the next line is:\n\t${data[CurTweetID - 1]}\n"
}

# a function for " = " option
function optionReadCurrent() 
{
    printf "The tweet at the current line is:\n\t${data[CurTweetID - 1]}\n"
}

# reading input file and storing it in an array
readarray data < tweetsmall.txt

CurTweetID=${#data[@]}

# repeating menu
while true; do
    
    printMenu
    read user_input

    case "$user_input" in

        c)  optionCreate
            ;;

        d)  printf "Type the line of the tweet you want to delete: "
            read userChoice

            checkIfInt $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            checkIfWithinBounds $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            optionDelete $userChoice
            ;;

        r)  printf "Type the line of the tweet you want to read: "
            read userChoice

            checkIfInt $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            checkIfWithinBounds $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            optionRead $userChoice
            ;;

        u)  printf "Type the line of the tweet you want to update: "
            read userChoice

            checkIfInt $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            checkIfWithinBounds $userChoice
            if [ $? -eq 1 ]; then
                continue
            fi
            optionUpdate $userChoice
            ;;

        $)  optionReadLast
            ;;

        -)  if [ $CurTweetID -eq 1 ]; then    
                printf "Error... Current tweet is the first on the file.\n\n"
                continue
            fi
            optionReadPrevious
            ;;

        +)  if [ $CurTweetID -eq ${#data[@]} ]; then    
                printf "Error... Current tweet is the last on the file.\n\n"
                continue
            fi
            optionReadNext
            ;;

        =)  optionReadCurrent
            ;;

        q)  printf "Exiting...\n"
            break
            ;;

        w)  printf "Writing to file...\n"
            printf "%s\n" "${data[@]}" > tweetsmall.txt
            ;;

        x)  printf "Writing to file and exiting...\n"
            printf "%s\n" "${data[@]}" > tweetsmall.txt
            break
            ;;

        *)  printf "Error... Input is not a valid option.\n\n" 
            ;;

    esac
done

exit 0
