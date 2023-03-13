import basic
import sys

while True:
    # text = input("basic >")
    # text = "-(1+1*2/1)"
    text = "1+1"
    res, error = basic.run("<stdin>", text)
    if error:
        print(error)
    else:
        print(res)
    sys.exit(0)