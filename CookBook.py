# Import our modules
import recipe.client as C
from recipe.color import color
import os
import configparser




# Initiate the config
CFG = configparser.RawConfigParser()
CFG.read( "config.ini" )






# Get values from the config
COLORMODE   =   CFG.getint(  "DEFAULT",    "COLORMODE",   fallback=0              )
DEBUGGER    =   CFG.getint(  "DEFAULT",    "DEBUGGER",    fallback=0              )
DATABASE    =   CFG.get(     "DEFAULT",    "DATABASE",    fallback="recipes.xml"  )





# Get the color class depending on the colormode that's set (see also: recipe.color)
# anything within the colors variable is dependant if the OS supports it. If the OS is windows, colormode will be OFF
colors = color(COLORMODE)


# Lambda function to clear the screen
cls = lambda: os.system('cls' if os.name=='nt' else 'clear')



if DEBUGGER == 1:
    print(f"{colors.WARNING}DEBUGGER:{colors.ENDC} {colors.OKGREEN}Successfully loaded config.{colors.ENDC}")


# Main class, do everything here that's not a constant, import or variable
def main():


    # Guard clause!
    # Clear our screen only if debugger is off
    if DEBUGGER == 0:
        cls()


    # Set the client (user object essentially; see also: recipe.client) and make it global to access in menu()
    global client
    client = C.Client(COLORMODE, DEBUGGER, DATABASE)


    # Welcome, user!
    print(f"""{colors.HEADER}   
                ############################################################
                ###############                              ###############
                ###############  Welcome to the Recipe Book  ###############
                ###############                              ###############
                ############################################################
        {colors.ENDC}""")


    # Call our menu
    menu()


def menu():


    # Give our user a choice of their potential options
    choice = input(f"""
                              {colors.HEADER}#################################{colors.ENDC}
                              {colors.HEADER}#                               #{colors.ENDC}
                              {colors.HEADER}#    A{colors.ENDC}: {colors.UNDERLINE}Create a recipe{colors.ENDC}         {colors.HEADER}#{colors.ENDC}
                              {colors.HEADER}#    B{colors.ENDC}: {colors.UNDERLINE}Search for a recipe{colors.ENDC}     {colors.HEADER}#{colors.ENDC}
                              {colors.HEADER}#    Q{colors.ENDC}: {colors.UNDERLINE}Close the book{colors.ENDC}          {colors.HEADER}#{colors.ENDC}
                              {colors.HEADER}#                               #{colors.ENDC}
                              {colors.HEADER}#################################{colors.ENDC}

                                  >>> """)


    # Switch block between the choices they make
    if choice.lower() == "a":


        # Guard clause!
        # Clear our screen only if debugger is off
        if DEBUGGER == 0:
            cls()


        # Give them a friendly message
        print(f"{colors.OKGREEN}{colors.UNDERLINE}Good choice!\n{colors.ENDC}")


        # Call the client's addRecipe function (see also: recipe.client)
        client.addRecipe()


        # Return to the menu
        menu()


    elif choice.lower() =="b":

        # Guard clause!
        # Clear our screen only if debugger is off
        if DEBUGGER == 0:
            cls()


        # Give them a friendly message
        print(f"{colors.OKGREEN}{colors.UNDERLINE}Ok!\n{colors.ENDC}")


        # Call the client's searchRecipe function (see also: recipe.client)
        client.searchRecipe()


        # Return to the menu
        menu()


    elif choice.lower() =="q":


        # Give them a friendly message
        print(f"{colors.OKGREEN}{colors.UNDERLINE}Goodbye!\n{colors.ENDC}")

        #EOF


    else:


        # Clear the screen; their choice was invalid
        # Guard clause!
        # Clear our screen only if debugger is off
        if DEBUGGER == 0:
            cls()


        # Give them a not-so-friendly message
        print(f"{colors.FAIL}Invalid option!")
        print(f"Please try again...{colors.ENDC}")


        # Reprint the menu
        menu()


if __name__ == '__main__':


    # Call the main function, however if at any time the user CTRL+C's, wish them goodbye
    try:


        main()


    except KeyboardInterrupt:


        # Guard clause!
        # Clear our screen only if debugger is off
        if DEBUGGER == 0:
            cls()

            
        print(f"\n\n{colors.HEADER}Goodbye!{colors.ENDC}\n")