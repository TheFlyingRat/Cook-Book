# Copyright (c) 2022 Joey M (TheFlyingRat)

from itertools import count
import xml.etree.ElementTree as ET
import os.path as path
from recipe.color import color


VERSION = 20220515.84


# Create a recipe object
class Recipe:
    # Init the class with defaults: debugger set to off; database set to recipes.xml
    def __init__( self, colorMode=0, debugger=0, database="recipes.xml" ):
        global colors
        colors = color(colorMode)
        

        # If the debugger is on, print... (global function)
        global printIfDebugger
        def printIfDebugger( textToPrint ):
            if debugger==1:
                print( f"{colors.WARNING}\nDEBUGGER: {textToPrint}\n{colors.ENDC}" )

        
                
        # Initialize the classname. Open the database (local variable) with read permissions. 
        self.database = database


        # Guard clause!
        # If the file does not exist, make it
        if not path.exists(self.database):
            printIfDebugger("Created new database!")
            f=open(self.database, "w")
            f.write("<root></root>")
            f.close()


        # Debugger mode
        if(debugger==1):
            import sys
            print(f"\n{colors.WARNING}")
            print("Debugger: On")
            print(f"Version: {VERSION}")
            print(f"Dictionary size: {path.getsize(self.database)}B")
            print(f"Dictionary name: {self.database}")
            print(f"Python version info: {sys.version}")
            print(f"Recipe module name: {__name__}")
            print(f"My path: {path.realpath(__file__)}")
            print(f"Path to interpreter: {sys.executable}")
            print(f"{colors.ENDC}")


        # Open the <root> of the XML database and set it's scope to the class
        self.XMLtree = ET.parse( self.database )
        self.XMLroot = self.XMLtree.getroot()


        printIfDebugger(f"{colors.OKGREEN}Successfully read the XML file and loaded root into memory.{colors.ENDC}")
            
            
            
            
    def addRecipe( self, recipeName, serves, ingredients, method ):


        printIfDebugger("Called add recipe")


        # Initialize the function scope variables
        tree = self.XMLtree
        root = self.XMLroot

        # Method preprocessing
        # Replace all ". " (end of sentences) with a carriage return.
        method = method.replace(". ", "\n  ")


        # Create a new child named "recipe" (<recipe>) **just as is (not within the <root> YET**
        # Thus, child would look like <recipe></recipe> right now and *not* <root>.....<recipe></recipe></root>
        child = ET.Element( "recipe" )


        # Guard clause!
        # If the recipe already exists, display the recipe to the user **then** return nothing to jump out of the function
        for recipe in self.XMLroot:
            if recipeName.lower() in recipe[0].text.lower():
                print( f"{colors.FAIL}The recipe already exists!\nHere's what it looks like: \n{colors.ENDC}" )
                self.searchRecipe(recipeName.lower())
                return

        # If the interpreter got up to here, it means it bypassed the duplicate checker

        # Create the children of the recipe
        ET.SubElement( child, "name" ).text = recipeName
        ET.SubElement( child, "serves" ).text = str( serves )
        
        
        # Create an element named ingredients (<ingredients>)
        ingredientsSubElement = ET.SubElement( child, "ingredients" )




        # For each ingredient (passed from function args), do...
        for ingredient in ingredients:


            # Inside the ingredients element (<ingredients)...
            ingredientSubElem = ET.SubElement( ingredientsSubElement, "ingredient" )


            # Add the ingredient name (<name>)
            ET.SubElement( ingredientSubElem, "name" ).text = ingredient


            # Add the ingredient amount (<amount>)
            ET.SubElement( ingredientSubElem, "amount" ).text = ingredients[ingredient] # Refer to the ingredients dict passed from func args, then find the index of "ingredient" (the name) to get it's value




        # Finally, add the method.
        ET.SubElement( child, "method" ).text = method


        # Append the child (<recipe>) to the root (<root>)
        # Thus, now it looks like <root>.....<recipe></recipe></root>
        root.append( child )


        # Set the indentation, so humans can read the database
        ET.indent( tree, space="\t", level=0 )


        # Finally, write it back to the disk
        tree.write( self.database )

        print( f"{colors.OKGREEN}Successfully wrote the recipe to the recipe book!{colors.ENDC}")
        
        
        
        
    def prepareIngredientDictionary( self, ingredients ):


        ingredientDictionary = {}


        # Ingredients is the <ingredients> tag.
        # Thus, ingredients[0] is *each* ingredient.
        # Thus, ingredients[0][0] is the ingredient name


        # So... for each *ingredient*...
        for ingredient in ingredients:


            # Append it's name and amount to a dictionary
            ingredientDictionary[ingredient[0].text] = ingredient[1].text


        # Return the dictionary
        return ingredientDictionary





    def searchRecipe( self, recipeInput ):


        printIfDebugger("Called search recipe")


        # For each child (recipe) in the XML's <root> element...
        for recipe in self.XMLroot:


            # If the user's input (in lowercase) matches any recipe name (in lowercase...)
            # child[0] is the first child (<name>) of the child variable (<recipe>)
            # Thus, "child" is a list of all <recipe>'s (see also: recipes.xml)
            # Colors is a class declared above. It makes the string processing look hard to read, but hey, at least it's beautiful.
            # I tried to keep the coloring "readable" to an extent. It's good enough, right?
            if recipeInput.lower() in recipe[0].text.lower():


                ingredientList = self.prepareIngredientDictionary(recipe[2])                                            # Set a cached variable with the function's return value so we don't have to call the function again; Hand it to a preprocessing function because it's an element (from the XML file) by itself
                

                print(f"{colors.HEADER}\n##################################################\n{colors.ENDC}")
                print(f"{colors.HEADER}Recipe: {colors.ENDC}{recipe[0].text}")
                print(f"{colors.HEADER}Serves: {colors.ENDC}{recipe[1].text}\n")
                print(f"{colors.HEADER}Ingredients: {colors.ENDC}({len(ingredientList)})") 

                
                for ingredient in ingredientList:                                                                       # For each ingredient in the cached dictionary...
                    print(f"  {colors.UNDERLINE}" + ingredientList[ingredient] + " of " + ingredient + colors.ENDC)     # print it out while being underlined!
                
                
                print(f"\n{colors.HEADER}Method: {colors.ENDC}\n  {recipe[3].text}")
                print(f"{colors.HEADER}\n##################################################\n{colors.ENDC}")

        print(f"{colors.HEADER}\n\n### You've reached the end ###\n\n{colors.ENDC}")