import os
import json
import time
from datetime import datetime
import logging 
import logging.config
from pathlib import Path


sizeOfFile = 0
createdlist= []

class FileHandler:

    def determine_chunks(size : int, chunksize : int) -> int: # determine in how many 10000 line chunks the file is to be seperated

        chunkmod = size % chunksize
        chunkdiv = size / chunksize

        if chunkdiv < 1:
            return 1
        elif chunkdiv < 10:
            mynum = int(str(chunkdiv)[:1])
        else:
            mynum = int(str(chunkdiv)[:2])

        if chunkmod == 0:
            return mynum
        else:
            return mynum + 1

    def read_from_json() -> list:

        global sizeOfFile
        curChunk = 0
        chunksize = 10000
        data = []

        with open("tweets.json", "r") as fp:
            curi = 0
            i = 0
            lines = fp.readlines() # get json to main memory
            sizeOfFile = len(lines)
            initsizeOfFile = sizeOfFile

            chunks = FileHandler.determine_chunks(sizeOfFile,chunksize)
            
            for line in reversed(lines): # reverse iterate
                obj = json.loads(line)
                data.append(obj)

                i+=1
                if i >= curi + chunksize: # every 10000 lines yield data
                    curi = i
                    curChunk += 1
                    if curChunk == chunks - 1 and (initsizeOfFile % chunksize) != 0: # calculate chunksize for the last chunk
                        chunksize = int(str(initsizeOfFile)[-4:])
                    
                    yield data

    def write_to_json(data : list, WoA : bool, createdlist : list):

        
        if WoA is True: # if there has been delete or update write from beggining, else append
            mydata = data[::-1] # reverse data for write
            with open("tweets.json", "w") as fp:
                for line in range(0, sizeOfFile):
                    fp.write(json.dumps(mydata[line]) + "\n")
        else:
            if len(createdlist) == 0:
                return
            else:
                with open("tweets.json", "a") as fp:
                    for line in range(len(createdlist)):
                        fp.write(json.dumps(createdlist[line]) + "\n")
                 

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

    def menu_handler(inp : str, genObject, fh : FileHandler, logfile : logging.Logger):

        global sizeOfFile
        delOrUpdated = False
        global createdlist
        
        data = next(genObject) # get first 10000 lines before anything
        currentTweet = sizeOfFile
        
        while True:
            
            if inp == "c":
                
                sizeOfFile += 1
                txt = input("\nPlease type in the text of the tweet you want to create: ")
                created_at_stamp = str(datetime.now())
                print("\nYour newly created tweet is:\n")

                data.insert(0,{"text": txt, "created_at": created_at_stamp}) # insert at beggining of list
                createdlist.append({"text": txt, "created_at": created_at_stamp})

                currentTweet = sizeOfFile 
                print(data[0]["text"] + ", " + data[0]["created_at"])
                logfile.info("Created a tweet at line: " + str(currentTweet))
                inp = "return to main menu"

            elif inp == "r":

                try:
                    i = int(input("\nPlease specify the number of the line you want to read: "))
                    if i < 1: raise IndexError()

                    while len(data) <= sizeOfFile - i: # get next 10000 until you reach te desired line
                        next(genObject)

                    print("\nThe tweet at line: " + str(i) + " is:\n")
                    print(data[sizeOfFile - i]["text"] + ", " + data[sizeOfFile - i]["created_at"])
                    logfile.info("Read the tweet at line: " + str(i))
                    currentTweet = i

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"
                    
            elif inp == "u":
                
                try:

                    j = int(input("\nPlease specify the number of the line you want to update: "))
                    if j < 1: raise IndexError()

                    while len(data) <= sizeOfFile - j: # get next 10000 until you reach te desired line
                        next(genObject)

                    print("\nThe tweet at line: " + str(j) + " is:\n")
                    print(data[sizeOfFile - j]["text"] + ", " + data[sizeOfFile - j]["created_at"])

                    txt = input("\nPlease enter the text that the updated tweet will contain: ")
                    created_at_stamp = str(datetime.now())
                    print("\nYour newly updated tweet is:\n")
                    data.remove(data[sizeOfFile - j])
                    data.insert(sizeOfFile - j, {"text": txt, "created_at": created_at_stamp})
                    print(data[sizeOfFile - j]["text"] + ", " + data[sizeOfFile - j]["created_at"])
                    logfile.info("Updated the tweet at line: " + str(j))
                    currentTweet = j
                    delOrUpdated = True

                except (ValueError, TypeError, IndexError):
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "d":

                delOrUpdated = True
                data.remove(data[sizeOfFile - currentTweet])
                print("Successfully deleted the current tweet.")
                logfile.info("Deleted the tweet at line: " + str(currentTweet))
                sizeOfFile -=1
                currentTweet -= 1
                inp = "return to main menu"

            elif inp == "$":
                
                currentTweet = sizeOfFile
                print("\nThe last tweet in the local file is:\n")
                print(data[sizeOfFile - currentTweet]["text"] + ", " + data[sizeOfFile - currentTweet]["created_at"])
                logfile.info("Read the last tweet in the local file")
                inp = "return to main menu"

            elif inp == "-":

                try:
                    if currentTweet == 1: raise Exception
                    print("\nThe tweet above the current one is:\n")
                    print(data[sizeOfFile - currentTweet + 1]["text"] + ", " + data[sizeOfFile - currentTweet + 1]["created_at"])
                    currentTweet -= 1
                    logfile.info("Read the previous tweet at line: " + str(currentTweet))
                    
                except IndexError:
                    next(genObject)
                    print("Try again.. need to load.")

                except Exception:
                    print("Invalid input, please try again.")
                    
                finally:
                    inp = "return to main menu"

            elif inp == "+":

                try:
                    if currentTweet == sizeOfFile: raise IndexError
                    print("\nThe tweet below the current one is:\n")
                    print(data[sizeOfFile - currentTweet - 1]["text"] + ", " + data[sizeOfFile - currentTweet - 1]["created_at"])
                    currentTweet += 1
                    logfile.info("Read the next tweet at line: " + str(currentTweet))

                except IndexError:
                    print("Invalid input, please try again.")

                finally:
                    inp = "return to main menu"

            elif inp == "=":
                
                print("\nThe current tweet is:\n")
                print(data[sizeOfFile - currentTweet]["text"] + ", " + data[sizeOfFile - currentTweet]["created_at"])
                logfile.info("Read the current tweet at line: " + str(currentTweet))
                inp = "return to main menu"        

            elif inp == "q":
                
                print("\nProgram Exited.")
                logfile.info("Exited without saving")
                break

            elif inp == "w":

                if(delOrUpdated):
                    while len(data) < sizeOfFile :
                        next(genObject)
                
                print("\nSaving changes (this might take a few seconds)..")
                fh.write_to_json(data, delOrUpdated, createdlist)
                createdlist.clear()
                delOrUpdated = False
                
                logfile.info("Saved the changes to the local data file")
                inp = "return to main menu"

            elif inp == "x":

                print("\nSaving changes (this might take a few seconds)..")
                if(delOrUpdated):
                    while len(data) < sizeOfFile :
                        next(genObject)


                fh.write_to_json(data, delOrUpdated, createdlist)
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
                print("\n- Returning back to main menu in 5 seconds. -------------------------")
                time.sleep(5)
                Utils.print_menu()
                inp = input("Type in your choice: ")


if __name__ == "__main__":

    print("\nWelcome!\n")
    data = FileHandler.read_from_json() # get generator object

    user = input("\nPlease type in your username and press enter: ")
    logging.config.fileConfig('myeditorlog.conf')
    logfile = logging.getLogger(user)

    Utils.print_menu()
    i = input("Type in your choice: ")
    Utils.menu_handler(i, data, FileHandler, logfile)
