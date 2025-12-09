# src/passgen/main.py

'''
IMPORT config
IMPORT password_generator as pg

FUNCTION choose_difficulty:
    PRINT difficulty menu (1, 2, 3)
    LOOP:
        READ user input as choice
        IF choice is "1" or "2" or "3":
            RETURN choice
        ELSE:
            PRINT "invalid choice" and repeat

FUNCTION ask_password_length:
    LOOP:
        ASK user to input desired length (show min, max and default)
        TRY to convert input to integer
            IF conversion fails:
                PRINT "invalid number" and continue
        IF length is smaller than MIN_LENGTH or larger than MAX_LENGTH:
            PRINT "must be between MIN and MAX" and continue
        RETURN length

FUNCTION handle_generate_password:
    PRINT "Generate password"
    CALL choose_difficulty -> level
    CALL ask_password_length -> length

    TRY:
        CALL pg.generate_password(length, level) -> password
        PRINT the resulting password
    EXCEPT ValueError as error:
        PRINT error message

IN run_app:
    IF choice == "1":
        CALL handle_generate_password()
    ELSE IF choice == "2":
            PRINT "TODO: show saved passwords (not implemented yet)"
    ELSE IF choice == "3":
            PRINT "Goodbye" and BREAK the loop
    ELSE:
            PRINT error message: "Invalid choice, try again"
'''

from . import config                    # import configuration (min/max/default length, paths, etc.)
from . import password_generator as pg  # import the password generator module
from . import storage                   # for saving/loading passwords

def print_header() -> None:
    '''
    Print a simple header for the CLI application.
    '''
    print('=' * 40)     # print a line of 40 "=" characters
    print('   PASSWORD GENERATOR (CLI)   ')     # title of the app
    print('=' * 40)     # print another line of 40 '='
    
    
def print_menu() -> None:
    '''
    Print the main menu options for the user.
    '''
    print('\nMenu:')
    print('1) Generate new password')
    print('2) Show saved passwords')
    print('3) Exit')
    

def choose_difficulty() -> str:
    '''
    Ask the user to choose a difficulty level for the password.
    Returns one of: "1", "2", "3".
    '''
    print('\nChoose difficulty level:')
    print('1) Easy      (letters + digits)')
    print('2) Medium    (letters + digits + some special characters)')
    print('3) Hard      (letters + digits + many special characters)')
    
    while True:
        choice = input('Difficulty (1-3): ').strip()
        
        if choice in ('1', '2', '3'):
            return choice   # valid choice, return it to the caller
        
        # if we reach this line, the input was invalid.
        print('❌ Invalid difficulty choice, please enter 1, 2 or 3.')
        
        
def ask_password_length() -> int:
    '''
    Ask the user for a password length.
    Validates that the length is an integer and within the allowed range
    defined in config.MIN_LENGTH and config.MAX_LENGTH.
    '''
    # build a helpful prompt that shows min/max and default values.
    prompt = (
        f'Enter password length '
        f'({config.MIN_LENGTH}-{config.MAX_LENGTH}, default {config.DEFAULT_LENGTH}): '
    )
    
    while True:
        raw = input(prompt).strip()
        
        # if the user just press Enter, we can use DEFAULT_LENGTH.
        if raw == '':
            return config.DEFAULT_LENGTH
        
        try:
            length = int(raw)   # try to convert the input to an integer
        except ValueError:
            print('❌ Invalid number, please enter an integer value.')
            continue    # go back to the beginning of the loop
        
        # now we check if the length is within the allowed range.
        if length < config.MIN_LENGTH or length > config.MAX_LENGTH:
            print(
                f'❌ Length must be between {config.MIN_LENGTH} and {config.MAX_LENGTH}.'
            )
            continue
        
        return length   # valid length, return it
    
    
def handle_generate_password() -> None:
    '''
    Handle the flow for the menu option 1: Generate a new password.
    - Ask for difficulty
    - Ask for length
    - Generate the password
    - Print the result
    - Optionally save the password to the JSON file
    '''
    print('\n--- Generate new password ---')
    
    # 1) ask the user which difficulty level to use.
    level = choose_difficulty()
    
    # 2) ask the user how long the password should be.
    length = ask_password_length()
    
    # 3) try to generate the password using the password_generator module.
    try:
        password = pg.generate_password(length, level)
    except ValueError as error:
        # if something goes wrong (e.g. invalid length or level),
        # we show an error message instead of crashing.
        print(f'❌ Error while generating password: {error}')
        return
    
    # 4) show the generated password to the user.
    print('\nYour new password is:')
    print(password)
    print()     # print an extra blank line for readability
    
    # 5) ask if the user wants to save the password.
    save_choice = input('Do you want to save this password? (y/n): ').strip().lower()
    
    if save_choice == 'y':
        # ask for additional information needed for storage
        service = input('Service name (e.g. Gmail, Spotify): ').strip()
        username = input('Username / email for this service: ').strip()
        
        # call the storage modul to save the new record
        storage.add_password(service, username, password)
        print('✅ Password saved.')
        print()
    else:
        print('Password was not saved.')
        print()


def handle_show_saved_passwords() -> None:
    '''
    Handle the flow for menu option 2: show all saved passwords.
    '''
    print('\n--- Saved passwords ---')
    
    records = storage.list_passwords()
    
    if not records:
        # if the list is empty, there are no saved passwords yet.
        print('No passwords have been saved yet.')
        print()
        return
    
    # loop over saved password records and print them nicely.
    for index, record in enumerate(records, start=1):
        service = record.get('service', '-')
        username = record.get('username', '-')
        password = record.get('password', '-')
        created_at = record.get('created_at', '-')
        
        print(f'{index}. Service: {service}')
        print(f'   Username: {username}')
        print(f'   Password: {password}')
        print(f'   Created:  {created_at}')
        print('-' * 40)
        
    print()     # extra blank line at the end
    
    
def run_app() -> None:
    '''
    Main application loop.
    - Shows the header once
    - Repeats the menu until the user chooses to exit
    '''
    print_header()      # show the title when the program starts
    
    while True:     #infinite loop until we break out of it
        print_menu()    # shows the menu options
        
        # asks the user to choose an option
        choice = input('Choose an option (1-3): ').strip()
        
        # handle the user´s choice
        if choice == '1':
            handle_generate_password()
            
        elif choice == '2':
            handle_show_saved_passwords()
            
        elif choice == '3':
            print('\nGoodbye! 👋')
            break
        
        else:
            # basic error handling for invalid menu choices
            print('\n❌ Invalid menu choice, please try again.\n')