"""# Required Libraries and Files"""

import pandas as pd
import spacy
import re
import spacy.cli

pipeline_name = 'en_core_web_sm'

# install the pipeline
spacy.cli.download(pipeline_name)

nlp = spacy.load(pipeline_name)#spacy's English model

"""# **No Crumbs Recipe Finder**

"""
df = pd.read_csv('recipes_data.csv', header=0)
#print(df)

#@title Main program
lines = "-"*40 # this variable is used throughout the code for better visibility

def select_category():
    # print diet options to the user
    print('Welcome to No Crumbs, your slayest recipe finder!')
    print("Please select a category:")
    print("[1] Vegetarian")
    print("[2] Vegan")
    print("[3] No restrictions")

    # and now we want the user's answer
    while True:
        diet_selection = input("Enter the number corresponding to your choice: ")
        try:
            category = int(diet_selection)
            if category in [1, 2, 3]:
                return category
            else: #in case they input a number higher than 3
                print("Invalid selection. Please enter a number between 1 and 3.")
        except ValueError: #in case the input is not a number
            print("Invalid input. Please enter a number.")

def get_input_ingredients():
    # we ask the user for the ingredients and the input given will be lowercased and
    # splited using the commas we very friendly asked them to use
    print(lines)
    return input("What ingredients do you have? (Please use commas to separate them)\n").lower().split(",")

def lemmatize(words):
    lemmatized_words = []
    for word in words:
        word = word.strip() #we eliminate unnecessary spaces
        doc = nlp(word)
        lemmatized_word = " ".join([token.lemma_ for token in doc])
        lemmatized_words.append(lemmatized_word)
    return lemmatized_words

def filter_recipes(df, ingredients, category):
    # separate the ingredients we want from the ones we don't want
    included_ingredients = []
    excluded_ingredients = []
    for ingredient in ingredients:
        ingredient = ingredient.lstrip() #we take away the space at the start of some ingredients
        if ingredient.startswith("-"):
            excluded_ingredients.append(ingredient.lstrip("-"))
        else:
            included_ingredients.append(ingredient)

    # we remove recipes containing excluded ingredients
    for excluded_ingredient in excluded_ingredients:
        df = df[~df['ingredients'].str.contains(re.escape(excluded_ingredient), case=False)]

    # we now choose the recipes that include all ingredients we want
    # depending on diet category selection
    if category == 1:
        filtered_df = df[(df['Vegetarian']) & (df['ingredients'].apply(lambda x: all(re.search(rf'{ingredient}', x, re.IGNORECASE) for ingredient in included_ingredients)))]
        #(breakdown of the line above)
        #to keep a recipe two conditions must apply: the recipe is categorized as vegetarian
        #the ingredients column contains all the ingredients listed
    elif category == 2:
        filtered_df = df[(df['Vegan']) & (df['ingredients'].apply(lambda x: all(re.search(rf'{ingredient}', x, re.IGNORECASE) for ingredient in included_ingredients)))]
    elif category == 3:
        filtered_df = df[(df['ingredients'].apply(lambda x: all(re.search(rf'{ingredient}', x, re.IGNORECASE) for ingredient in included_ingredients)))]
    else:
        filtered_df = pd.DataFrame(columns=df.columns)

    return filtered_df.head(10) #to not overwhelm the user we only keep maximum 10 of the results

#Main program
while True:
    category = select_category() #the user choses diet preference
    input_ingredients = get_input_ingredients() #the user inputs list of ingredients they want
    lemmatized_input = lemmatize(input_ingredients) #the list of ingredients is lemmatized
    filtered_recipes = filter_recipes(df, input_ingredients, category) #we search for matching recipes to diet category and containing all ingredients

    if filtered_recipes.empty: #in case no matching recipes are found we ask if they want to try again
        change_category = input("Sorry, no recipes found matching your criteria. Would you like to start again? (yes/no): ").lower()
        print(lines)
        if change_category == "yes" or change_category == "y":
            continue  # restart the loop if the user wants to start again
        else:
            break  # exit the loop if the user doesn't want to start again
    else:
        print(lines)
        #first we print the results from the filtering
        print("Here are some recipes containing your ingredient(s) (up to 10):")
        #we want the recipe titles shown to be enumerated
        for i, (_, row) in enumerate(filtered_recipes.iterrows(), start=1):
            print(f"{i}. {row['title']}")

        print(lines)

        #we let the user select the recipe they are interested in
        selection = input("Select a recipe number to view its ingredients:\n")
        try:
            #we make sure the number selected is the correct one, keeping in mind python starts at 0
            selected_recipe_index = int(selection) - 1
            if 0 <= selected_recipe_index < len(filtered_recipes): #the user should have written a number over 0 and under 11
                selected_recipe = filtered_recipes.iloc[selected_recipe_index:selected_recipe_index + 1]
                ingredients = eval(selected_recipe['ingredients'].iloc[0]) #we get the ingredients for the choosen recipe
                directions = eval(selected_recipe['directions'].iloc[0])#and the  instructions
                #we print all the information in a easily readable format
                print('\n***', selected_recipe['title'].iloc[0], '***')
                print()
                print(f"Ingredients:")
                for ingredient in ingredients:
                    print("-", ingredient.strip())
                print()
                print(f"Instructions:")
                for direction in directions:
                    print("-", direction.strip())
            else:
                print("Invalid selection.") #again we account for incorrect input number
        except ValueError:
            print("Invalid input. Please enter a number.") #or for incorrect type input

        print(lines)
        #lastly we give the option to start again or finish the search
        restart = input("Would you like to start again? (yes/no): ").lower()
        if restart == "yes" or restart == "y":
            continue
        else:
            break # Exit the loop if the user doesn't want to start again

print(lines)
print("Thank you for using No Crumbs! :)")
