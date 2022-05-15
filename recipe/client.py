# Copyright (c) 2022 Joey M (TheFlyingRat)
from recipe.color import color
from os import name as Name
class Client:
    def __init__( self, colorMode=0, debugger=0, database="recipes.xml" ):
        global colors
        colors = color(colorMode)


        # If the debugger is on, print... (global function)
        global printIfDebugger
        def printIfDebugger( textToPrint ):
            if debugger==1:
                print( f"{colors.WARNING}\nDEBUGGER: {textToPrint}\n{colors.ENDC}" )


        # Guard-ish clauses, tell user the color warnings
        if colorMode == 1 and Name=="nt":
            print(f"WARN: Color mode is ON but you're on windows. Color mode will be turned off.")
        if colorMode == 1 and not Name=="nt":
            print(f"NOTICE: Color mode is ON. Turn it back off if terminal is malformed")
        if colorMode == 2:
            print(f"WARN: Color mode is FORCED. Turn it back off if terminal is malformed")
        if colorMode == 0:
            printIfDebugger(f"Color mode is OFF") 


        # Import the recipe object with debugger flag set to the debugger flag of this class
        import recipe.recipe as R
        self.r = R.Recipe( colorMode=colorMode, debugger=debugger, database=database )





    def queryIngredients( self ):

        # Initialize fresh dictionary
        ingredientList = {}


        # **VALIDATE** the first ingredient, as it's a constraint. Minimum of 1 ingredient, so check if its empty...
        ingredient = self.validateInputs(   input(f"{colors.HEADER}What ingredients? I will ask for the amount after this question{colors.ENDC} >>> ")   )
        amount = self.validateInputs(   input(f"{colors.HEADER}How much?{colors.ENDC} >>> ")   )


        # Put it in the dictionary
        ingredientList[ingredient] = amount


        # While infinity....
        while True:


            # Ask user for what ingredient **not validated; can be empty**
            ingredient = input(f"{colors.HEADER}What ingredients?{colors.ENDC} >>> ")


            # Guard clause!
            # If it's empty...
            if not ingredient:
                # Get us out of here returning the current list
                return ingredientList 


            # However if we bypass the guard clause, ask the user how much of the specified ingredient **VALIDATED** to prevent empties
            amount = self.validateInputs(   input(f"{colors.HEADER}How much?{colors.ENDC} >>> ")   )


            # Append it to the dictionary
            ingredientList[ingredient] = amount


            # Question: Why don't we return here? We cannot, as we can only break the loop if the next ingredient is nothing. 





    def addRecipe( self ):

        # Ask the user for their data
        name        = self.validateInputs(   input(f"{colors.HEADER}Name of your recipe?{colors.ENDC} >>> ")   )
        servings    = self.validateInputs(   input(f"{colors.HEADER}How many does it serve? Number only{colors.ENDC} >>> "), checkIfInt=1   )
        ingredients = self.queryIngredients() # Ingredient loop...
        method      = self.validateInputs(   input(f"{colors.HEADER}What's the method? Seperate each instruction by a new sentence{colors.ENDC} >>> ")   )


        printIfDebugger(name)
        printIfDebugger(servings)
        printIfDebugger(ingredients)
        printIfDebugger(method)

        # Send it to the database!
        self.sendToDatabase( name, servings, ingredients, method )
    


    def sendToDatabase ( self, name, servings, ingredients, method ):

        # Send to the database using the recipe book class
        self.r.addRecipe( name, servings, ingredients, method )




    def searchRecipe( self ):

        # Search for recipe from recipe.py
        searchKeyword = input(f"{colors.HEADER}What's for dinner? Press enter to show all recipes{colors.ENDC} >>> ")   
        self.r.searchRecipe(searchKeyword)
    
    
    
    
    
    def validateInputs( self, value, checkIfInt=0 ):

        # Guard clauses!
        # Validate the user's data
        if not value:                                                                       # If the value is empty...
            import sys
            sys.exit(f"{colors.FAIL}EXCEPTION: Value cannot be none!{colors.ENDC}")         # Exit with exception
        if ( checkIfInt==1 ):                                                               # If flag checkIfInt (arg) is 1...
            try:
                return int(value)                                                           # Try to make it an int, because user inputs are always strings
            except:
                import sys
                sys.exit(f"{colors.FAIL}EXCEPTION: Must be a number!{colors.ENDC}")         # Except, if it can't exit with exception
        
        # If we passed the checks, return the original value!
        return value