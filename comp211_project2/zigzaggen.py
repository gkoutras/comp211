import os, sys

def main():  

    TREE_DEPTH_UPPER_LIMIT = 10
    TREE_WIDTH = 2

    # expecting two initial arguements (sys.argv[0] is the name of the program and sys.argv[1] is the the tree depth)
    if len(sys.argv) != 2:
        print(os.strerror(f"Usage: {sys.argv[0]} # processes"))
        os._exit(1)
    
    # specifying tree depth from the second argument be no more than 10
    tree_depth = int(sys.argv[1])
    if tree_depth > TREE_DEPTH_UPPER_LIMIT: 
        print(os.strerror("Depth should be no more than 10."))
        os._exit(1)

    # root process
    print(f"Level 0 of the zig zag path - I am process with PID = {os.getpid()}, and I am the root.")

    child_pid = 0
    for i in range(tree_depth):
        i += 1

        for j in range(TREE_WIDTH):

            # forking child
            child_pid = os.fork()

            # checking if fork failed
            if child_pid == -1:
                print(os.strerror("Failed to fork."))
                os._exit(1)

            # children processes
            if child_pid == 0:
                # checking if level is an even number
                if i % 2 == 0:
                    if j == 0:
                        # exitting from the left child, if level is an even number
                        print(f"Level {i} of the zig zag path - I am process with PID = {os.getpid()}, my parent is PID = {os.getppid()}, and I am its left child.")
                        os._exit(1)
                    else:
                        # carrying on from the right child, if level is an even number
                        print(f"Level {i} of the zig zag path - I am process with PID = {os.getpid()}, my parent is PID = {os.getppid()}, and I am its right child.")
                        break
                # checking if level is an odd number
                else:
                    if j == 0:
                        # carrying on from the left child, if level is an odd number
                        print(f"Level {i} of the zig zag path - I am process with PID = {os.getpid()}, my parent is PID = {os.getppid()}, and I am its left child.")
                        break
                    else:
                        # exitting from the right child, if level is an odd number
                        print(f"Level {i} of the zig zag path - I am process with PID = {os.getpid()}, my parent is PID = {os.getppid()}, and I am its right child.")
                        os._exit(1)
            else:
              os.wait
        
        # separating previously forked children from newly forked ones
        if child_pid != 0:
            break
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
    