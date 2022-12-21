# COMP211 Project 2

Linux Commands, Bash Scripting, Process Programming

## Task 1: Linux Commands
### - linuxCommands.ipynb

3. Via `head -11 tweetsmall.txt | cat >> tmp.txt`, the first 11 lines of the input file `tweetsmall.txt` are concatenated appendingly (`>>`) with an empty helper file `tmp.txt`. Via `echo "I love TUC" >> tmp.txt`, a new text is added to line 12 (`>>`) of `tmp.txt`. Via `tail -3157 tweetsmall.txt | cat >> tmp.txt`, the last 3158 lines of `tweetsmall.txt` are concatenated appendingly (`>>`) with `tmp.txt`. These commands connect with each other with the `&&` operator, which means that each of them waits for a successful execution from its predecessors in order for itself to run. All of these commands similarly connect (`&&`) with the `cat tmp.txt > tweetsmall.txt` command, which takes the contents of `tmp.txt` and overwrites them (`>`) into `tweetsmall.txt`. Finally, the `tmp.txt` helper file is deleted with the `rm` command.
4. Same as the previous question, but instead of adding a text line in the selected line number with `echo`, that line number is utterly omitted. 

## Task 2: Bash Script - Twitter Viewer & Editor
### - twitterViewerEditor.sh



## Task 3: Bash Script - Sentiment Analyser
### - twitterSentimentAnalyzer.sh

At frst, the lines of the input files `positive.txt` and `negative.txt` are loaded with the command `readarray` in the memory in corresponding indexed arrays, from where they can be called inside the program. Through `if [ -f $out_file ]`, it is checked if the output file `sentimentpertweet.txt` already exists in the directory, and if the condition is true, then it is deleted with the `rm` command, so that the new results are not appended to the existing ones produced by previous executions. A `while` loop is then called, which runs for each line of the main input file `tweetsmall.txt`. Here the code `line_arr=($(echo $line | tr -cs 'a-zA-Z' ' '))` is called, which does the following: For the `–cs` option, the `tr` command will search and replace the non-alphabetic characters (`a-zA-Z`) with the space character, the current `line` will then be updated by whatever is produced, and thanks to this syntax, each of the words that now make up the line will be printed via `echo` to the corresponding array element of `line_arr`, ignoring spaces. Since `line_arr` now consists of one word in each of its elements, a `for` loop is called that runs for each element, with two more nested ones that run for each of the elements of the `positive` and `negative` arrays respectively. In the internal ones, each word of `line_arr` is checked with all words loaded into the input arrays, and if there is a match via the `if [ $i == $j ]` condition, then the `sentiment` variable is either incremented, or decreased. Thus, as soon as the loops are finished, i.e. as soon as an entire tweet-line has been checked, depending on whether this variable has received a final positive or negative or zero value, the corresponding message is finally printed in the output file `sentimentpertweet.txt`. When the `while` loop finishes, then all lines of the main input file `tweetsmall.txt` have been checked, and the sentiment analysis is completed.

## Task 4: Python Process Programming - Zig Zag Process Generator
### - zigzaggen.py

At first, after checking for the correct number of arguments, which are the name of the executable and the tree depth number (`sys.argv[0]` and `sys.argv[1]` respectively), as well as the upper limit that can be chosen for the maximum depth, the root process prints its relevant information. Then, two nested `for` loops begin. The outer one runs along the depth of the tree, while the inner one runs along the level width, which is 2 at each level. Once `os.fork()` is executed, a check is made for the possibility of branching failure, followed by some `if` conditions, intended to separate the produced children. Via `if child_pid == 0`, only the children produced at this point in the loop get to continue. Through `if i % 2 == 0` and `if i % 2 == 1`, it is checked whether the number of the current level is even or odd. Through `if j == 0` and `if j == 1`, it is checked whether the child at this level is on the left or right position relative to its father. Depending on the requested combinations of the above conditions, each child, after printing its relevant information, will either terminate with `os._exit(1)`, or exit the width loop with `break` to carry on to the depth loop, for it to become the new parent. Finally, to avoid forking a process with a difference of more than one level from its parent, a `break` called with the condition `if child_pid != 0`, so that any process that already has two children can completely break out from the outer loop.

## Task 5: Python Pipes - Three-Way Pipe Implementation
### - threewaypipe.py

