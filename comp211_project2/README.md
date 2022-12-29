# COMP211 Project 2

Linux Commands, Bash Scripting, Process Programming

## Task 1: Linux Commands
*- linuxCommands.ipynb*

1. The `tail` command places a pointer to the last line of the file `tweetsmall.txt` and takes as an argument the offset from there, in this case `-1` for the last line.

2. The `head` command just like `tail`, places a pointer to the first line of the file `tweetsmall.txt`. With offset `-11`, the first part of the command returns the first 11 lines of the file, which are pipelined (`|`) as input to a `tail` command, where with offset `-1`, it returns the last line of the taken input, in this case line 11 of the file.

3. Via `head` and arguement `-11`, the first 11 lines of the input file `tweetsmall.txt` are pipelined and concatenated with a `cat` command appendingly (`>>`) in an empty helper file `tmp.txt`. Via `echo`, a new text is added to line 12 of `tmp.txt`. Via `tail` and arguement `-3157`, the last 3158 lines of `tweetsmall.txt` are pipelined and concatenated with a `cat` command  appendingly (`>>`) in `tmp.txt`. These linked commands connect with each other with the `&&` operator, which means that each of them waits for a successful execution from its predecessors in order for itself to run. All of these commands similarly connect with the a final `cat` command, which takes the contents of `tmp.txt` and overwrites them (`>`) into `tweetsmall.txt`. Finally, the `tmp.txt` helper file is deleted with the `rm` command.

4. Same as the previous question, but instead of adding a text line in the selected line number with `echo`, that line number is omitted.

5. The `cat` command with a double redirection operator (`>>`), appends to the given filestream instead of overwritting.

6. Using `cut` commands, the second and fourth words of `tweetsmall.txt` are retrieved, separated by spaces (`" "`). Via `paste` the desired stream is created, where the outputs of `cut` are separated with `";"`. The output of `paste` is pipelined (`|`) to the command `sort`, where after the delimiter is declared with `-t` `";"`, the field based on which the sorting is done is also declared. This is why `+1` is chosen, so that `sort` gets plus one position from the first field of the input line. Whatever is generated is given as input to `cat` which redirects it to a new file `onlytwowords.txt`

7. Line 200 was taken from `tweetsmall.txt` just as in previous task, and given as input to the `wc` command where with `-w` argument it returned the number of words.

8. Via `grep` command, lines are case-insensitively (`-i`) searched for the word (`-w`) "romney". The lines to be returned are given as input to another inverse (`-v`) `grep`, which leaves out the lines with the word "obama" case-insensitively (`-i`) again. The final result is pipelined (`|`) to a `cat` command, that redirects it to a new `romney.txt` file.

9. .

10. Via `mkdir` command, a `alltxts` directory is created. Upon successful execution (`&&`) of the previous command, an `mv` command is executed, which transfers all files ending with `.txt` from the current directory to `alltxts`. Then all the permissions for user (`u`), group (`g`) and others (`o`) are given with `chmod` in the directory `alltxts`, `cd` is done in `alltxts` and all the permissions are given there permissions for all files ending with `.txt`.

## Task 2: Bash Script - Twitter Viewer & Editor
*- twitterViewerEditor.sh*

The implementation of the Twitter Viewer & Editor was done in a similar way as in the previous project, this time Bash Script instead of Python. Specifically, a `while true` loop was used again for the menu handler. Just before the loop, the `tweetsmall.txt` input file is read with a `readarray` command, and all its lines are passed into an array `data`. Functions have been used for each menu option, taking as an argument, where necessary, the input entered by the user. The array `data` and `CurTweetID`, a variable that symbolizes the current tweet the user is in, are treated as global variables. Apart from the functions that implement the options of the program, two additional functions were also written, that check the user's input. Specifically, in one case it is checked if the input is an integer, and then if the requested number is within the limits of the array `data`. The cases in which the user might try to read next tweet with `+` option while being on the last tweet of the array, or respectively if they try to read previous tweet with `-` option while being on the first, are checked as well. The `w` and `x` options were implemented with the `printf` command and the `>` operator, so that contents of the array `data` are overwritten into the input file `tweetsmall.txt`. In each case, the `CurTweetID` variable was updated accordingly.

## Task 3: Bash Script - Sentiment Analyser
*- twitterSentimentAnalyzer.sh*

At frst, the lines of the input files `positive.txt` and `negative.txt` are loaded with the command `readarray` in the memory in corresponding indexed arrays, from where they can be called inside the program. Through `if [ -f $out_file ]`, it is checked if the output file `sentimentpertweet.txt` already exists in the directory, and if the condition is true, then it is deleted with the `rm` command, so that the new results are not appended to the existing ones produced by previous executions. A `while` loop is then called, which runs for each line of the main input file `tweetsmall.txt`. Here the code `line_arr=($(echo $line | tr -cs 'a-zA-Z' ' '))` is called, which does the following: For the `–cs` option, the `tr` command will search and replace the non-alphabetic characters (`a-zA-Z`) with the space character, the current `line` will then be updated by whatever is produced, and thanks to this syntax, each of the words that now make up the line will be printed via `echo` to the corresponding array element of `line_arr`, ignoring spaces. Since `line_arr` now consists of one word in each of its elements, a `for` loop is called that runs for each element, with two more nested ones that run for each of the elements of the `positive` and `negative` arrays respectively. In the internal ones, each word of `line_arr` is checked with all words loaded into the input arrays, and if there is a match via the `if [ $i == $j ]` condition, then the `sentiment` variable is either incremented, or decreased. Thus, as soon as the loops are finished, i.e. as soon as an entire tweet-line has been checked, depending on whether this variable has received a final positive or negative or zero value, the corresponding message is finally printed in the output file `sentimentpertweet.txt`. When the `while` loop finishes, then all lines of the main input file `tweetsmall.txt` have been checked, and the sentiment analysis is completed.

## Task 4: Python Process Programming - Zig Zag Process Generator
*- zigzaggen.py*

At first, after checking for the correct number of arguments, which are the name of the executable and the tree depth number (`sys.argv[0]` and `sys.argv[1]` respectively), as well as the upper limit that can be chosen for the maximum depth, the root process prints its relevant information. Then, two nested `for` loops begin. The outer one runs along the depth of the tree, while the inner one runs along the level width, which is 2 at each level. Once `os.fork()` is executed, a check is made for the possibility of branching failure, followed by some `if` conditions, intended to separate the produced children. Via `if child_pid == 0`, only the children produced at this point in the loop get to continue. Through `if i % 2 == 0` and `if i % 2 == 1`, it is checked whether the number of the current level is even or odd. Through `if j == 0` and `if j == 1`, it is checked whether the child at this level is on the left or right position relative to its father. Depending on the requested combinations of the above conditions, each child, after printing its relevant information, will either terminate with `os._exit(1)`, or exit the width loop with `break` to carry on to the depth loop, for it to become the new parent. Finally, to avoid forking a process with a difference of more than one level from its parent, a `break` called with the condition `if child_pid != 0`, so that any process that already has two children can completely break out from the outer loop.

## Task 5: Python Pipes - Three-Way Pipe Implementation
*- threewaypipe.py*

