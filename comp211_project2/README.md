# COMP211 Project 2

Linux Commands, Bash Scripting, Process Programming

## Task 1



## Task 2



## Task 3: Bash Script - Sentiment Analyser



## Task 4: Python Process Programming - Zig Zag Process Generator

At first, after checking for the correct number of arguments, which are the name of the executable and the tree depth number (`sys.argv[0]` and `sys.argv[1]` respectively), as well as the upper limit that can be chosen for the maximum depth, the root process prints its relevant information. Then, two nested `for` loops begin. The outer one runs along the depth of the tree, while the inner one runs along the level width, which is 2 at each level. Once `os.fork()` is executed, a check is made for the possibility of branching failure, followed by some `if` conditions, intended to separate the produced children. Via `if child_pid == 0`, only the children produced at this point in the loop get to continue. Through `if i % 2 == 0` and `if i % 2 == 1`, it is checked whether the number of the current level is even or odd. Through `if j == 0` and `if j == 1`, it is checked whether the child at this level is on the left or right position relative to its father. Depending on the requested combinations of the above conditions, each child, after printing its relevant information, will either terminate with `os._exit(1)`, or exit the width loop with `break` to carry on to the depth loop, for it to become the new father.

## Task 5


