def print_pattern():
    string = input("Enter a string: ")
    if string:
        for i in range(1, len(string) + 1):
            print(string[:i])
    else:
        print("kaya...\nKaya bak rahe ho madherchod...????")

print_pattern()

