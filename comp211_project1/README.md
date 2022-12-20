# COMP211 Project 1

Software Development for a Twitter Viewer & Editor using Python Tools.

## Develepment Phase

For this phase, all the starting code of the program was written for the first phase of its development.  

When starting the program, and after the necessary modules/libraries have been installed, two instances of the "Utils" and "FileHandler" classes are created respectively. Then by calling the `read_from_json()` function of the "FileHandler" class, the "text" and "created_at" attributes of all the tweets found in the json file are assigned to a list. At this point, a list of the data we need from the tweets is stored in the main memory. Then the menu is printed on the console, by calling the `print_menu()` function of the "Utils" class and the user's input is read. Then the `menu_handler()` function of the "Utils" class is called with its arguments being the list of tweets located in the main memory, the input given by the user and the instance of the "FileHandler" class that has been created, and then the execution flow is passed to the code of `menu_handler()`.

## Logging Phase

For this phase, continuing from Development Phase, when using the tool, the actions/commands used by the last user who ran it should be logged in a "logme.txt" file. INFO has to basically be logged, through a suitable ".conf" file in the following format:  

`format = %(asctime)s - %(name)s - %(levelname)s - %(message)s`

The "myeditorlog.conf" file was implemented as follows:

- The configurations of this file concern file handlers, so that the appropriate actions are recorded in a "logme.txt" file in appending mode and at DEBUG level. Appending mode was selected so that log entries continue to be recorded, even if shutdown and restart of the program has occurred in between.

The code for this phase was modified as follows:

- At first, the user is asked to provide a username, which will be used for the log entries of his actions, while the logging gets its configurations from the "myeditorlog.conf" file. Then, inside the `menu_handler()` for each of the actions offered by the program, an entry is made in the "logme.txt" file with the corresponding information. Finally, the user is given the ability to select "l" from the menu to display in the console all the entries logged up until that time in the file.

## Profiling Phase

*note: This phase was not implemented as a ".py" file, but rather as an ".ipynb" file, for easier connections between many small script cells.*

For this phase, continuing from Logging Phase, parts of the code with temporal or spatial liabilities had to be found and profiled. Because of this `read_from_json()`, `write_to_json()` and `menu_handler()` functions were emphasized.

At first, in order for the code to be examined more easily and without user input, the already existing code for the Logging Phase was modified. The new code runs all menu options with custom input, so commandes that offer temporal or spatial liabilities can be determined. Apparently, of all the options, "w" and "x" options consume more time, since both access the disk (`write_to_jason()`). Great emphasis was also placed on the `read_from_jason()` function which plays a big part for the smooth operation of the program. THis function takes up more memory space but also consumes more time than `write_to_json()` since it not only accesses the disk, reading from json file, but also writes the entire file to the data list in main memory.

Some indicative diagnostics are the following:

- `read_from_json()`:
    - `cProfile` in IDE: 11.929 seconds 
    - `lprun` in notebook: 31.3154 seconds
        - `obj = json.loads(line)`
        - 92% of total time
        - 299999 hits
    - `prun` in collab: 31.199 seconds
    - peak memory: 7442.75 MiB, increment: 2793.99 MiB
- `write_to_json()`:
    - `cProfile` in IDE: 9.317 seconds
    - `lprun` in collab: 20.1396 seconds
        - `fp.write(json.dumps(data[line]) + "\n")`
        - 98.7% of total time
    - `prun` in collab: 19.863 seconds
    - peak memory: 4659.22 MiB, increment: 0.27 MiB

## Refactoring Phase

For this phase, continuing from Profiling Phase, the refactored code is modified from the logging code and has the following improvements:

- Reading 300000 tweets directly is no longer viable, since this method was quite time consuming and often unnecessary. This is achieved by converting the `read_from_json()` function to a generator function. At first, `read_from_json()` with `readlines()` passes the contents of the json file to main memory to iterate in memory and not on disk, as was the case in the original code. `read_from_json()` is always called once at the beginning of the program and returns the last 10000 tweets for the user to edit (like practically when a user opens his twitter, a page with the most recent tweets is shown). With the modifications in this phase, the tweets are read from the json file in chunks of 10000, starting from the end of the file which ensured a much faster operation for the 'c' & '$' menu options, since the file does not need to be fully loaded. In the event that the user needs a tweet, via read or update, in a line that has not been read yet, the program will call the generator as many times as it takes to reach that line, so that it is written in the list located in the central memory and which manages tweets within the program. Thus, the refactored code manages to take only the needed amount of time for its functions. At worst, it will take as much time in total as it took at the beginning of the Development Phase, since the generator function will be exhausted.
- Existing tweets are no longer overwritten in the json file when selecting 'w' or 'x' option form the menu, since this method was quite time consuming and often unnecessary as well. Only newly created tweets are appended to the end of the file, making it more efficient in both time and memory. Though, if a delete or an update has been called between the lines of the file, then the entire file is overwritten, similar to the original code from the Develepment Phase.

## Unit Testing Phase

For this phase, continuing from Refactoring Phase, Unit Tests had to be implemented in order for the final refactored code to be examined as to the correctness of its results.

At first, in order for the code to be examined more easily and without user input, the already existing code for the Refactoring Phase was modified. The new code runs all menu options with custom input combinations for the needs of the unit tests. There are also two tests, checked by `determine_chunks()' which resulted from the refactored code, and check if the creation of the chunks is done successfully in the borderline cases. (check chunk size, check chunk size after creation).

Specifically, tests were carried out for the following cases:
- (=/q), (-/=), (-/q), (-/+), (r/q), (\$/q), (c/q), (\$,q), (c/q), (\$/q), (d/q), (\$/q), (d/x), (\$/q), (check chunk size), (check chunk size after create), ( u/q), (r/q), (u/w), (r/q)

*note: The json file has to be in its initial form, for the tests to run correctly.*