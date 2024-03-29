# -*- coding: utf-8 -*-
"""NoCrumbs_NLP3.ipynb

Original file is located at
    https://colab.research.google.com/drive/1Mlpy9tu9RCccgUC20B2u6Z0vEEPCrnZi
"""

"""# Required Libraries and Files"""

import zipfile
import gdown
import pandas as pd
from tqdm import tqdm

print("Downloading Dataset zip...")
output = "archive.zip"
id = "10-NuS-prcLNZjlXSqQd6RBOM44k8epdx" #dataset file
gdown.download(id=id, output=output)
print("Done!")



"""# Load Dataset"""

#@title Unzip the dataset file
print("Unzipping...")
with zipfile.ZipFile('archive.zip', 'r') as zip_ref:
    zip_ref.extractall()

#@title Build the dataframe
print("Creating data frame...")
df = pd.read_csv('recipes_data.csv', header=0)

#eliminating duplicated recipes with the same name
df = df.drop_duplicates(subset='title')

#we randomize the recipes
random_state = 42
df = df.sample(frac=1, random_state=random_state) #random_state for reproducibility

#we drop the columns that we won't need
hide_columns = ['site', 'source', 'site', 'link']
df = df.drop(columns=hide_columns)

# We keep only the first 500.000 recipes so the code runs faster,
# feel free to change the parameter to your preference
number_of_recipes = 500000
df = df.head(number_of_recipes)

#@title Anotate vegetarian and vegan recipes
print("Annotating diet preferences...")

non_veggie = ['chicken', 'beef', 'pork', 'fish', 'lamb', 'goat', 'meat', 'turkey', 'duck', 'veal', 'bacon', 'ham', 'salmon', 'copa',
              'shrimp', 'crab', 'lobster', 'oyster', 'sardine', 'anchovy', 'trout', 'tuna', 'mutton', 'venison', 'sole', 'jamon',
              'squid', 'octopus', 'clams', 'scallops', 'jelly', 'jell-o', 'jello', 'gelatin', 'rabbit', 'deer', 'quail', 'pepperoni',
              'snail', 'horse', 'buffalo', 'boar', 'guinea pig', 'kangaroo', 'ostrich', 'pigeon', 'turtle', 'frog', 'hamburguer',
              'alligator', 'elk', 'snake', 'sausage', 'pancetta', 'filet', 'chorico', 'ribs', 'chorizo', 'cod', 'meatballs', 'herring']

non_vegan = non_veggie + ['milk', 'butter', 'cream', 'cheese', 'yogurt', 'honey', 'whey', 'casein',
                           'beeswax', 'isenglass', 'carmine', 'shellac', 'albumin', 'cochineal',
                           'collagen', 'ghee', 'lanolin', 'suet', 'rennet', 'lard', 'buttermilk',
                           'squalene', 'taurine', 'egg', 'yolk', 'whey', 'casein', 'ghee', 'curd',
                           'paneer', 'lactose', 'quark', 'kefir', 'cottage', 'mascarpone', 'brie']

def is_vegetarian(ingredient):
    return all(i not in ingredient for i in non_veggie)

def is_vegan(ingredient):
    return all(i not in ingredient for i in non_vegan)


total_rows = len(df)

tqdm.pandas(desc="Processing rows")
df['Vegetarian'] = df['ingredients'].progress_apply(lambda x: all(is_vegetarian(ingredient) for ingredient in x.split(', ')))
df['Vegan'] = df['ingredients'].progress_apply(lambda x: all(is_vegan(ingredient) for ingredient in x.split(', ')))

print("Done!")


#print the df to visualize how the data looks
#print(df)


df.to_csv("recipes_data.csv", index=False)
