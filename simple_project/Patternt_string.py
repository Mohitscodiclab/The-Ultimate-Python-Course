def print_pattern():
    string = input("Enter a string: ")
    for i in range(1, len(string) + 1):
        print(string[:i])

print_pattern()
