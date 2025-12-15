# src/passgen/main.py

'''
IMPORT config
IMPORT password_generator as pg
IMPORT storage
IMPORT utils

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
        CALL handle_show_saved_passwords()
    ELSE IF choice == "3":
        PRINT "Goodbye" and BREAK the loop
    ELSE:
        PRINT error message: "Invalid choice, try again"
'''

from rich.console import Console        # for colored / styled output
from rich.panel import Panel            # for a nice box around the header
from rich.table import Table

from . import config                    # import configuration (min/max/default length, paths, etc.)
from . import password_generator as pg  # import the password generator module
from . import storage                   # for saving/loading passwords
from . import utils                     # input helper functions
from . import logger                    # logging module
from .security import mask_password     # import security

# create a global Console instance that we can use throughout this module.
console = Console()

def print_header() -> None:
    '''
    Print a colorful header for the CLI application using Rich.
    '''
    title_text = (
        '[bold magenta]PassGen[/bold magenta]\n'
        '[cyan]Password Generator CLI[/cyan]'
        )
    
    # panel creates a nice box around the text
    panel = Panel(
        title_text,
        border_style='magenta',
        expand=False,
    )
    
    console.print(panel)
    
    
def print_menu() -> None:
    '''
    Print the main menu options for the user using Rich for nicer styling.
    '''
    console.print('\n[bold underline]Menu[/bold underline]', style='cyan')
    console.print('[green]1)[/green] Generate new password')
    console.print('[green]2)[/green] Show saved passwords')
    console.print('[green]3)[/green] Exit')
    

def choose_difficulty() -> str:
    '''
    Ask the user to choose a difficulty level for the password.
    Returns one of: "1", "2", "3".
    '''
    console.print('\n[bold underline]Choose difficulty level:[/bold underline]', style='cyan')
    console.print('[green]1)[/green] Easy      (letters + digits)')
    console.print('[green]2)[/green] Medium    (letters + digits + some special characters)')
    console.print('[green]3)[/green] Hard      (letters + digits + many special characters)')
    
    while True:
        choice = input('Difficulty (1-3): ').strip()
        
        if choice in ('1', '2', '3'):
            return choice   # valid choice, return it to the caller
        
        # if we reach this line, the input was invalid.
        console.print('❌ [red]Invalid difficulty choice, please enter 1, 2 or 3.[/red]')
        
        
def ask_password_length() -> int:
    '''
    Ask the user for a password length using the utils.ask_int helper.
    Uses the default length from config if the user just presses Enter.
    '''
    prompt = (
        f'Enter password length '
        f'({config.MIN_LENGTH}-{config.MAX_LENGTH}, default {config.DEFAULT_LENGTH}): '
    )
    
    # we delegate the actual validation and input parsing to utils.ask_int.
    length = utils.ask_int(
        prompt=prompt,
        min_value=config.MIN_LENGTH,
        max_value=config.MAX_LENGTH,
        default=config.DEFAULT_LENGTH,
    )
    return length
    
    
def handle_generate_password() -> None:
    '''
    Handle the flow for the menu option 1: Generate a new password.
    - Ask for difficulty
    - Ask for length
    - Generate the password
    - Print the result
    - Optionally save the password to the JSON file
    '''
    console.print('\n--- Generate new password ---', style='bold cyan')
    
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
        console.print(f'❌ [red]Error while generating password:[/red] {error}')
        # log the error
        logger.log_event(f'Error generating password: {error}", level="ERROR')
        return
    
    # log that a password was generated (without storing the actual password).
    logger.log_password_generated(length=length, difficulty=level)
    
    # 4) show the generated password to the user.
    console.print('\nYour new password is:', style='bold green')
    console.print(f'[bold]{password}[/bold]')
    print()     # print an extra blank line for readability
    
    # 5) ask if the user wants to save the password.
    save_choice = input('Do you want to save this password? (y/n): ').strip().lower()
    
    if save_choice == 'y':
        # ask for additional information needed for storage using utils.ask_non_empty.
        service = utils.ask_non_empty('Service name (e.g. Gmail, Spotify): ')
        username = utils.ask_non_empty('Username / email for this service: ')
        
        # call the storage modul to save the new record
        storage.add_password(service, username, password)
        
        # log that we saved the password (without the password itself).
        logger.log_password_saved(service=service, username=username)
        
        console.print('✅ Password saved.', style='green')
        print()
    else:
        console.print('Password was not saved.', style='yellow')
        print()


def handle_show_saved_passwords() -> None:
    '''
    Handle the flow for menu option 2: show all saved passwords.
    '''
    console.print('\n--- Saved passwords ---', style='bold cyan')
    
    records = storage.list_passwords()
    
    # log how many records we are about to show.
    logger.log_passwords_listed(count=len(records))
    
    if not records:
        # if the list is empty, there are no saved passwords yet.
        console.print('No passwords have been saved yet.', style='yellow')
        print()
        return
    
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('#', style='dim', width=4)
    table.add_column('Service')
    table.add_column('Username')
    table.add_column('Password (masked)')
    table.add_column('Created", style="cyan')
    
    # loop over saved password records and print them nicely.
    for index, record in enumerate(records, start=1):
        service = record.get('service', '-')
        username = record.get('username', '-')
        password = record.get('password', '-')
        created_at = record.get('created_at', '-')
        
        # mask the password before printing (to avoid showing full secret in CLI).
        masked = mask_password(password, visible_chars=3)
        
        table.add_row(
            str(index),
            service,
            username,
            masked,
            created_at,
        )
        
    print(table)
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
        choice = utils.ask_menu_choice('Chooce an option (1-3): ')
        
        # handle the user´s choice
        if choice == '1':
            handle_generate_password()
            
        elif choice == '2':
            handle_show_saved_passwords()
            
        elif choice == '3':
            console.print('\nGoodbye! 👋', style='bold magenta')
            break
        
        else:
            # basic error handling for invalid menu choices
            console.print('\n❌ Invalid menu choice, please try again.\n', style='red')