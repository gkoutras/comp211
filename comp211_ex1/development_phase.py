import json
import time
from datetime import datetime


class FileHandler:

    """
    A class to handle the reading from and writing to the json file.
    """

    def read_from_json() -> list:

        data = []
        
        with open("tweets.json", "r") as fp:
            for line in fp:
                obj = json.loads(line)
                data.append(obj)

        return data

    def write_to_json(data : list):

        with open("tweets.json", "w") as fp:
            for line in range(0, len(data)):
                fp.write(json.dumps(data[line]) + "\n")


class Utils:

    """ 
    A class that contains two utility functions: 
        -A simple print_menu function that prints the options 
         the user has once the application is set up to the console.
        -The main menu_handler() function that performs all the possible actions
         a user can choose from the main menu that is printed.
    """

    def print_menu():

        """
        A basic function that prints the options a user has once the app is set up.
        """

        print("\nWelcome to a simple Twitter Viewer and Editor!")
        print("Below is a list of options that can be performed based on your input:\n")
        print(" ' c ' creates a tweet")
        print(" ' d ' deletes a tweet")
        print(" ' r ' reads a tweet")
        print(" ' u ' updates a tweet")
        print(" ' $ ' reads the last tweet on file")
        print(" ' - ' reads the previous tweet")
        print(" ' + ' reads the next tweet")
        print(" ' = ' prints current tweet")
        print(" ' q ' close the application")
        print(" ' w ' (over) write file to secondary storage memory(disk)")
        print(" ' x ' save changes to the local file and close the application\n")

    def menu_handler(inp : str, data : list, fh : FileHandler):

        """
        A function that performs every possible action chosen from the user 
        once the app has been set up.
        """

        currentTweet = len(data) 

        while True:

            if inp == "c":

                txt = input("\nPlease type in the text of the tweet you want to create: ")
                created_at_stamp = str(datetime.now())
                print("\nYour newly created tweet is:\n")             
                data.append({"text": txt, "created_at": created_at_stamp})
                currentTweet = len(data)
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                inp = "return to main menu"

            elif inp == "r":

                try:
                    i = int(input("\nPlease specify the number of the line you want to read: "))
                    if i < 1: raise IndexError()
                    print("\nThe tweet at line: " + str(i) + " is:\n")
                    print(data[i - 1]["text"] + ", " + data[i - 1]["created_at"])
                    currentTweet = i

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "u":

                try:
                    j = int(input("\nPlease specify the number of the line you want to update: "))
                    if j < 1: raise IndexError()
                    print("\nThe tweet at line: " + str(j) + " is:\n")
                    print(data[j - 1]["text"] + ", " + data[j - 1]["created_at"])

                    txt = input("\nPlease enter the text that the updated tweet will contain: ")
                    created_at_stamp = str(datetime.now())
                    print("\nYour newly updated tweet is:\n")
                    data.remove(data[j - 1])
                    data.insert(j - 1, {"text": txt, "created_at": created_at_stamp})
                    print(data[j - 1]["text"] + ", " + data[j - 1]["created_at"])
                    currentTweet = j

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "d":

                data.remove(data[currentTweet - 1])
                print("Successfully deleted the current tweet.")
                currentTweet -= 1
                inp = "return to main menu"

            elif inp == "$":

                currentTweet = len(data)
                print("\nThe last tweet in the local file is:\n")
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                inp = "return to main menu"

            elif inp == "-":

                try:
                    if currentTweet == 1: raise IndexError
                    print("\nThe tweet above the current one is:\n")
                    currentTweet -= 1
                    print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])

                except IndexError:
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "+":

                try:
                    print("\nThe tweet below the current one is:\n")
                    print(data[currentTweet]["text"] + ", " + data[currentTweet]["created_at"])
                    currentTweet += 1

                except IndexError:
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "=":
                
                print("\nThe current tweet is:\n")
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                inp = "return to main menu"

            elif inp == "q":

                print("\nProgram Exited.")
                break

            elif inp == "w":

                print("\nSaving changes (this might take a few seconds)..")
                fh.write_to_json(data)
                inp = "return to main menu"

            elif inp == "x":

                print("\nSaving changes (this might take a few seconds)..")
                fh.write_to_json(data)
                print("\nProgram Exited.")
                break

            else:
                print("\n- Returning back to main menu in 5 seconds. -------------------------")
                time.sleep(5)
                Utils.print_menu()
                inp = input("Type in your choice: ")


if __name__ == "__main__":

    print("\nWelcome!\n")
    print("Opening input file (this might take a few seconds)..")
    data = FileHandler.read_from_json()

    Utils.print_menu()
    i = input("Type in your choice: ")
    Utils.menu_handler(i, data, FileHandler)
