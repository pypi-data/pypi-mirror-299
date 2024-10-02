import pyfiglet

def shell():
    # Creare un titolo in ASCII art con il font "slant"
    ascii_title = pyfiglet.figlet_format("basic-gear", font="slant")
    print(ascii_title)

    print("Welcome to the basic-gear interctive shell. Type 'exit' to close.")

    while True:
        command = input(">>> ").strip().split()

        if command[0].lower() == 'exit':
            print("Bye")
            break
