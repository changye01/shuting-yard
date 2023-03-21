import main

while True:
    text = input("basic >")
    # text = "1+1"
    res, error = main.run("<stdin>", text)
    if error:
        print(error)
    else:
        print(res)
