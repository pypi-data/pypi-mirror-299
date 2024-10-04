import argparse
import re
import pyfiglet

# local imports
import basic_gear.core.cffi_interface as cffi_interface
import basic_gear.core.tor_checks as tor_checks

def shell():
    # Create an ASCII art title with the "slant" font
    ascii_title = pyfiglet.figlet_format("basic-gear", font="slant")
    print(ascii_title)

    print("Welcome to the basic-gear interactive shell. Type 'exit' to close.")

    while True:
        command = input(">>> ").strip()

        if command.lower() == 'exit':
            print("Bye")
            break

        match = re.match(r'(\d+\.?\d*)\s*([+\-*/%])\s*(\d+\.?\d*)', command)
        if match:
            a, operator, b = match.groups()
            a, b = float(a), float(b)

            try:
                if operator == '+':
                    print(cffi_interface.add(a, b))
                elif operator == '*':
                    print(cffi_interface.multiply(a, b))
                elif operator == '-':
                    print(cffi_interface.subtract(a, b))
                elif operator == '/':
                    print(cffi_interface.divide(a, b))
                elif operator == '%':
                    print(cffi_interface.mod(a, b))
            except Exception as e:
                print(f"Error: {e}")
        else:
            parser = argparse.ArgumentParser(prog='basic-gear-shell', description="basic-gear interactive shell")
            subparsers = parser.add_subparsers(dest='command')

            parser_create_channel = subparsers.add_parser('create_channel', help='Create a Tor channel')
            parser_create_channel.add_argument('port', type=int, help='Port number for the channel')

            parser_tor = subparsers.add_parser('tor', help='Check if Tor is installed')

            try:
                args = parser.parse_args(command.split())

                if args.command == 'create_channel':
                    cffi_interface.create_channel(args.port)
                    print(f'Channel created at port {args.port}')

                elif args.command == 'tor':
                    tor_checks.check_tor_installed()
                    
            except SystemExit:
                pass
            except Exception as e:
                print(f"Error: {e}")

