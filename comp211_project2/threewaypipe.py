import os, sys

def main(): 

    MESSAGES = ("I love PLH211", "the professor is boring", "but the subject is", "interesting & useful")
    TREE_WIDTH = 2

    # setting reader and writer in the returned tuples of pipes p0 and p1
    p0 = os.pipe()
    p1 = os.pipe()

    # checking if pipes p0 and p1 failed
    if not (p0 and p1):
        print(os.strerror("Failed to execute pipe."))
        os.close(p0)
        os.close(p1)
        os._exit(1)
    
    for i in range(TREE_WIDTH):

        # forking child
        child_pid = os.fork()

        # checking if fork failed
        if child_pid == -1:
            print(os.strerror("Failed to execute fork."))
            os.close(p0)
            os.close(p1)
            os._exit(1)

        # checking if process is a child
        if child_pid == 0:
            # checking if process is on left side
            if i == 0:
                # left child setting p0[0] reader and printing info
                os.close(p0[1])
                for message in MESSAGES:
                    read_message = os.read(p0[0], len(message))
                    print(f"I am process with PID = [{os.getpid()}], my parent has PID = [{os.getppid()}], and I read \"{read_message.decode()}\".")
                os.close(p0[0])
                os._exit(0)
            # checking if process is on right side
            else:
                # right child setting p1[0] reader and printing info
                os.close(p1[1])
                for message in MESSAGES:
                    read_message = os.read(p1[0], len(message))
                    print(f"I am process with PID = [{os.getpid()}], my parent has PID = [{os.getppid()}], and I read \"{read_message.decode()}\".")
                os.close(p1[0])
                os._exit(0)
        else:
            # parent waiting for child process to complete
            os.wait

    # checking if process is the parent
    if child_pid != 0:
        # parent setting p0[1] and p1[1] writers and printing info
        os.close(p0[0])
        os.close(p1[0])
        for message in MESSAGES:
            os.write (p0[1], message.encode())
            os.write (p1[1], message.encode())
            print(f"I am process with PID = [{os.getpid()}], I am the parent, and I write \"{message}\".")
        os.close(p0[1])
        os.close(p1[1])
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
    