def read(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as err:
        print(err.strerror)

def readlines(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for n, line in enumerate(file.readlines()):
                print(n + 1, line, end="")
    except FileNotFoundError as err:
        print(err.strerror)



def writelines(filename, arr):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(arr)
    except OSError as err:
        print(err.strerror)


writelines("file.txt", [str(x)+'\n' for x in range(10, 60, 10)])
readlines("file.txt")