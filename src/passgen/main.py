# src/passgen/main.py

'''
FUNCTION print_header:
    PRINT a nice title and separator lines

FUNCTION print_menu:
    PRINT the available menu options
        1) Generate new password
        2) Show saved passwords
        3) Exit

FUNCTION run_app:
    CALL print_header

    LOOP forever:
        CALL print_menu
        READ user input as choice (string)
        
        IF choice == "1":
            PRINT "TODO: generate password (not implemented yet)"
        ELSE IF choice == "2":
            PRINT "TODO: show saved passwords (not implemented yet)"
        ELSE IF choice == "3":
            PRINT "Goodbye" and BREAK the loop
        ELSE:
            PRINT error message: "Invalid choice, try again"
'''

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
        choice = input('Choose un option (1-3): ').strip()
        
        # handle the user´s choice
        if choice == '1':
            # here we will later call the real password generation logic
            print('\n[TODO] Generate password is not implemented yet. \n')
            
        elif choice == '2':
            # here we will later show saved passwords from the JSON file
            print('\n[TODO] Show save passwords is not implemeneted yet. \n')
            
        elif choice == '3':
            # exit the loop and end the application
            print('\nGoodbye! 👋')
            break
        
        else:
            # basic error handling for invalid menu choices
            print('\n❌ Invalid menu choice, please try again.\n')