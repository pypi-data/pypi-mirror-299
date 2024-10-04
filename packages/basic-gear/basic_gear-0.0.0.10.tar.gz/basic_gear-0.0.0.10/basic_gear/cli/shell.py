import argparse
import re
import pyfiglet

# local imports
import basic_gear.core.cffi_interface as cffi_interface
import basic_gear.core.tor_checks as tor_checks


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

        parser = argparse.ArgumentParser(prog='basic-gear-shell', description="basic-gear interctive shell")

        """
        # Aggiungiamo i sottocomandi per le diverse operazioni
        subparsers = parser.add_subparsers(dest='command')

        # Definizione del sottocomando 'somma'
        parser_sum = subparsers.add_parser('sum', help='Add two float numbers')
        parser_sum.add_argument('a', type=int, help='First number')
        parser_sum.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'multiply'
        parser_multiply = subparsers.add_parser('multiply', help='Add two float numbers')
        parser_multiply.add_argument('a', type=int, help='First number')
        parser_multiply.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'subtract'
        parser_subtract = subparsers.add_parser('subtract', help='Add two float numbers')
        parser_subtract.add_argument('a', type=int, help='First number')
        parser_subtract.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'divide'
        parser_divide = subparsers.add_parser('divide', help='Add two float numbers')
        parser_divide.add_argument('a', type=int, help='First number')
        parser_divide.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'mod'
        parser_mod = subparsers.add_parser('mod', help='Add two float numbers')
        parser_mod.add_argument('a', type=int, help='First number')
        parser_mod.add_argument('b', type=int, help='Second numer')

        # Definizione del sottocomando 'create_channel'
        parser_create_channel = subparsers.add_parser('create_channel', help='create a tor channels')
        parser_create_channel.add_argument('port', type=int, help='port')

        parser_sum_expressiom = subparsers.add_parser('sum_expression', help='Add two float numbers')
        parser_sum_expressiom.add_argument('expression', type=str, help='Espressione da calcolare, es. 3+5')
        """
        parser.add_argument('expression', type=str, help='Expression to calculate, e.g. 3+5 or 5-3, etc.')

        match = re.match(r'(\d+\.?\d*)\s*([+\-*/%])\s*(\d+\.?\d*)', args.expression)

        if not match:
            print("Error: invalid expression. You must provide two numbers with an operator in between.")
        else:
            a, operator, b = match.groups()
            a, b = float(a), float(b)

        try:

            # Parsing dell'input dell'utente
            args = parser.parse_args()

            if operator == '+':
                print(cffi_interface.add(a, b))

            elif operator == '*':
                print(cffi_interface.multiply(args.a, args.b))

            elif operator == '-':
                print(cffi_interface.subtract(args.a, args.b))

            elif operator == '/':
                print(cffi_interface.divide(args.a, args.b))

            elif operator == '%':
                print(cffi_interface.mod(args.a, args.b))
            
            elif operator == 'create_channel':
                cffi_interface.create_channel(args.port)
                print(f'channel created at port {args.psort}')

            elif args.command == 'tor':
                tor_checks.check_tor_installed()
            
            else:
                print("Command not recognized.")

        except SystemExit:
            # Gestione per evitare che argparse chiuda la shell su errore
            pass
        except Exception as e:
            print(f"Error: {e}")
