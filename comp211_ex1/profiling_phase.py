import os
import json
import time
from datetime import datetime
import logging 
import logging.config
from pathlib import Path
import cProfile 


class FileHandler:

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

    def print_menu():

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

        print(" *' l ' check logging info*\n")

    def menu_handler(inp : str, data : list, fh : FileHandler, logfile : logging.Logger):

        currentTweet = len(data)
        
        while True:

            if inp == "c":

                #txt = input("\nPlease type in the text of the tweet you want to create: ")
                txt='bob'
                created_at_stamp = str(datetime.now())
                print("\nYour newly created tweet is:\n")
                data.append({"text": txt, "created_at": created_at_stamp})
                currentTweet = len(data)
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                logfile.info("Created a tweet at line: " + str(len(data)))
                inp = "return to main menu"

            elif inp == "r":

                try:
                    #i = int(input("\nPlease specify the number of the line you want to read: "))
                    i = 10
                    if i < 1: raise IndexError()
                    print("\nThe tweet at line: " + str(i) + " is:\n")
                    print(data[i - 1]["text"] + ", " + data[i - 1]["created_at"])
                    logfile.info("Read the tweet at line: " + str(i))
                    currentTweet = i

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"
                    
            elif inp == "u":

                try:
                    #j = int(input("\nPlease specify the number of the line you want to update: "))
                    j = 10
                    if j < 1: raise IndexError()
                    print("\nThe tweet at LINEE: " + str(j) + " is:\n")
                    print(data[j - 1])

                    #txt = input("\nPlease enter the text that the updated tweet will contain: ")
                    txt = 'bob'
                    created_at_stamp = str(datetime.now())
                    print("\nYour newly updated tweet is:\n")
                    data.remove(data[j - 1])
                    data.insert(j - 1, {"text": txt, "created_at": created_at_stamp})
                    print(data[j - 1]["text"] + ", " + data[j - 1]["created_at"])
                    logfile.info("Updated the tweet at line: " + str(j))
                    currentTweet = j

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "d":

                data.remove(data[currentTweet - 1])
                print("Successfully deleted the current tweet.")
                logfile.info("Deleted the tweet at line: " + str(currentTweet))
                currentTweet -= 1
                inp = "return to main menu"

            elif inp == "$":
                
                currentTweet = len(data)
                print("\nThe last tweet in the local file is:\n")
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                logfile.info("Read the last tweet in the local fileee")
                inp = "return to main menu"

            elif inp == "-":

                try:
                    if currentTweet == 1: raise IndexError
                    print("\nThe tweet above the current one is:\n")
                    currentTweet -= 1
                    print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                    logfile.info("Read the previous tweet at line: " + str(currentTweet))
                    
                except IndexError:
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "+":

                try:
                    print("\nThe tweet below the current one is:\n")
                    print(data[currentTweet]["text"] + ", " + data[currentTweet]["created_at"])
                    currentTweet += 1
                    logfile.info("Read the next tweet at line: " + str(currentTweet))

                except IndexError:
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "=":
                
                print("\nThe current tweet is:\n")
                print(data[currentTweet - 1]["text"] + ", " + data[currentTweet - 1]["created_at"])
                logfile.info("Read the current tweet at line: " + str(currentTweet))
                inp = "return to main menu"        

            elif inp == "q":
                
                print("\nProgram Exited.")
                logfile.info("Exited without saving")
                break

            elif inp == "w":

                print("\nSaving changes (this might take a few seconds)..")
                fh.write_to_json(data)
                logfile.info("Saved the changes to the local data file")
                inp = "return to main menu"

            elif inp == "x":

                print("\nSaving changes (this might take a few seconds)..")
                fh.write_to_json(data)
                print("\nProgram Exited.")
                logfile.info("Saved changes to the local file and exited")
                break

            elif inp == "l":

                print("\nLogging info:\n")
                loggingLines = Path("logme.txt").read_text().splitlines()
                for line in loggingLines:
                    print(line)
                inp = "return to main menu"

            else:
               break


if __name__ == "__main__":

    print("\nWelcome!\n")
    print("Opening input file (this might take a few seconds)..")

    data = FileHandler.read_from_json()

    logging.config.fileConfig('myeditorlog.conf')
    logfile = logging.getLogger('bob')

    options = ['c','r','u','d','=','+','-','$','w','x']
    for option in options :
            Utils.menu_handler(option,data,FileHandler,logfile)
            