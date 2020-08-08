#! /usr/bin/env python
#  -*- coding: utf-8 -*-
# ======================================================
#     template1.py
#  ------------------------------------------------------
# Created for Full Circle Magazine Issue #160
# Written by G.D. Walters
# Copyright (c) 2020 by G.D. Walters
# This source code is released under the MIT License
# ======================================================

import sys
import os
import platform
import datetime
import sqlite3
from PIL import ImageTk, Image
from dbutils import quote
from fpdf import fpdf
from fpdf import FPDF
from fpdf import Template

# ======================================================
dbname = "./tests/database/cookbook.db"
imagepath = "./tests/database/recipeimages/"

# The recipe information for the two sample recipes are defined as follows.  These have been extracted
# from the actual database tables and converted into lists...
# ======================================================
recipe_table_dat = []
ingredients_table_dat = []
instructions_table_dat = []
cats_table_dat = []
images_table_dat = []

rtd = (
    166, 'Mongolian Beef and Spring Onions',
    'https://www.allrecipes.com/recipe/201849/mongolian-beef-and-spring-onions/',
    '4 serving(s)', '30 minutes', 5, 1, None,
    'A soy-based Chinese-style beef dish. Best served over soft rice noodles or rice.',
    1)
recipe_table_dat.append(rtd)
# ingredients table
ing = [(1802, 166, None, None, None, '2 teaspoons vegetable oil'),
       (1803, 166, None, None, None, '1 tablespoon finely chopped garlic'),
       (1804, 166, None, None, None, '1/2 teaspoon grated fresh ginger root'),
       (1805, 166, None, None, None, '1/2 cup soy sauce'),
       (1806, 166, None, None, None, '1/2 cup water'),
       (1807, 166, None, None, None, '2/3 cup dark brown sugar'),
       (1808, 166, None, None, None,
        '1 pound beef flank steak, sliced 1/4 inch thick on the diagonal'),
       (1809, 166, None, None, None, '1/4 cup cornstarch'),
       (1810, 166, None, None, None, '1 cup vegetable oil for frying'),
       (1811, 166, None, None, None,
        '2 bunches green onions, cut in 2-inch lengths')]
ingredients_table_dat.append(ing)
# instructions
instructions_table_dat.append((
    157, 166,
    'Heat 2 teaspoons of vegetable oil in a saucepan over medium heat, and cook and stir the garlic and ginger until they release their fragrance, about 30 seconds. Pour in the soy sauce, water, and brown sugar. Raise the heat to medium-high, and stir 4 minutes, until the sugar has dissolved and the sauce boils and slightly thickens. Remove sauce from the heat, and set aside.\nPlace the sliced beef into a bowl, and stir the cornstarch into the beef, coating it thoroughly. Allow the beef and cornstarch to sit until most of the juices from the meat have been absorbed by the cornstarch, about 10 minutes.\nHeat the vegetable oil in a deep-sided skillet or wok to 375 degrees F (190 degrees C).\nShake excess cornstarch from the beef slices, and drop them into the hot oil, a few at a time. Stir briefly, and fry until the edges become crisp and start to brown, about 2 minutes. Remove the beef from the oil with a large slotted spoon, and allow to drain on paper towels to remove excess oil.\nPour the oil out of the skillet or wok, and return the pan to medium heat. Return the beef slices to the pan, stir briefly, and pour in the reserved sauce. Stir once or twice to combine, and add the green onions. Bring the mixture to a boil, and cook until the onions have softened and turned bright green, about 2 minutes.\n\n'
))
# Cats
cats_table_dat.append([(166, 'Asian'), (166, 'Beef'), (166, 'Main Dish')])
# Images
images_table_dat.append((95, 166, './MongolianBeefandSpringOnions.png'))

# Amish White Bread
recipe_table_dat.append((
    154, 'Amish White Bread',
    'https://www.allrecipes.com/recipe/6788/amish-white-bread/',
    '24 serving(s)', '150 minutes', 4, 1, None,
    "I got this recipe from a friend. It is very easy, and doesn't take long to make.\n",
    1))
ingredients_table_dat.append([
    (1669, 154, None, None, None,
     '2 cups warm water (110 degrees F/45 degrees C)'),
    (1670, 154, None, None, None, '2/3 cup white sugar'),
    (1671, 154, None, None, None, '1 1/2 tablespoons active dry yeast'),
    (1672, 154, None, None, None, '1 1/2 teaspoons salt'),
    (1673, 154, None, None, None, '1/4 cup vegetable oil'),
    (1674, 154, None, None, None, '6 cups bread flour')
])
instructions_table_dat.append((
    145, 154,
    'In a large bowl, dissolve the sugar in warm water, and then stir in yeast. Allow to proof until yeast resembles a creamy foam.\nMix salt and oil into the yeast. Mix in flour one cup at a time. Knead dough on a lightly floured surface until smooth. Place in a well oiled bowl, and turn dough to coat. Cover with a damp cloth. Allow to rise until doubled in bulk, about 1 hour.\nPunch dough down. Knead for a few minutes, and divide in half. Shape into loaves, and place into two well oiled 9x5 inch loaf pans. Allow to rise for 30 minutes, or until dough has risen 1 inch above pans.\nBake at 350 degrees F (175 degrees C) for 30 minutes.\n\n\n'
))
cats_table_dat.append([(154, 'Breads'), (154, 'Breads')])
images_table_dat.append((79, 154, './AmishWhiteBread.png'))

# "Crack" Chicken
recipe_table_dat.append((
    366, 'Crack Chicken', 'https://www.dinneratthezoo.com/crack-chicken/', '6',
    '4 hours 5 minutes', '4.5', 1, None,
    "This crack chicken is creamy ranch flavored chicken that's cooked in the crock pot until tender. A super easy slow cooker recipe that only contains 3 ingredients.\n",
    1))
ingredients_table_dat.append([
    (4821, 366, None, None, None, '2 lbs boneless skinless chicken breasts'),
    (4822, 366, None, None, None, '1 ounce packet ranch seasoning'),
    (4823, 366, None, None, None, '16 ounces cream cheese cut into cubes'),
    (4824, 366, None, None, None,
     'cooked crumbled bacon and green onions for serving optional')
])
instructions_table_dat.append((
    361, 366,
    'Place the chicken breasts, ranch seasoning and cream cheese in a slow cooker.\nCook on HIGH for 4 hours or LOW for 6-8 hours.\nShred the chicken with two forks. Stir until everything is thoroughly combined.\nServe, topped with bacon and green onions if desired.\n'
))
cats_table_dat.append([(366, 'American'), (366, 'Chicken'), (366, 'Main Dish'),
                       (366, 'Sandwich')])
images_table_dat.append((319, 366, './CrackChicken.png'))
# End of recipe information defination

# Template...
elements = [
    {
        'name': 'header',
        'type': 'T',
        'x1': 17.0,
        'y1': 8.0,
        'x2': 0,
        'y2': 0,
        'font': 'Arial',
        'size': 8,
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
    },
    {
        'name': 'title',
        'type': 'T',
        'x1': 17,
        'y1': 26,
        'x2': 0,
        'y2': 0,
        'font': 'Arial',
        'size': 22,
        'bold': 1,
        'italic': 1,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
    },
    {
        'name': 'recipeimage',
        'type': 'I',
        'x1': 17,
        'y1': 25,
        'x2': 80,
        'y2': 89,
        'font': None,
        'size': 0,
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': 'image',
        'priority': 2,
    },
    {
        'name': 'ingreidentshead',
        'type': 'T',
        'x1': 17,
        'y1': 220,
        'x2': 0,
        'y2': 0,
        'font': 'Arial',
        'size': 12,
        'bold': 1,
        'italic': 1,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': 'Ingredients:',
        'priority': 2,
    },
    {
        'name': 'ingredientitems',
        'type': 'W',
        'x1': 17,
        'y1': 115,
        'x2': 90,
        'y2': 400,
        'font': 'Arial',
        'size': 11,
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': True
    },
    {
        'name': 'instructionhead',
        'type': 'T',
        'x1': 17,
        'y1': 360,
        'x2': 0,
        'y2': 0,
        'font': 'Arial',
        'size': 12,
        'bold': 1,
        'italic': 1,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': 'Instructions:',
        'priority': 2,
    },
    {
        'name': 'instructions',
        'type': 'W',
        'x1': 17,
        'y1': 185,
        'x2': 160,  # 200,
        'y2': 400,  # 400,
        'font': 'Arial',
        'size': 11,
        'bold': 0,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 1,
        'multiline': True
    },
    {
        'name': 'description',
        'type': 'T',
        'x1': 85,
        'y1': 28,
        'x2': 200,
        'y2': 35,
        'font': 'Arial',
        'size': 12,
        'bold': 1,
        'italic': 1,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': True
    },
    {
        'name': 'source',
        'type': 'T',
        'x1': 85,
        'y1': 60,
        'x2': 200,
        'y2': 66,
        'font': 'Arial',
        'size': 10,
        'bold': 1,
        'italic': 1,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': True
    },
    {
        'name': 'servings',
        'type': 'T',
        'x1': 26,
        'y1': 95,
        'x2': 84,
        'y2': 98,
        'font': 'Arial',
        'size': 10,
        'bold': 1,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': False
    },
    {
        'name': 'time',
        'type': 'T',
        'x1': 86,
        'y1': 95,
        'x2': 145,
        'y2': 98,
        'font': 'Arial',
        'size': 10,
        'bold': 1,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': False
    },
    {
        'name': 'rating',
        'type': 'T',
        'x1': 148,
        'y1': 95,
        'x2': 200,
        'y2': 98,
        'font': 'Arial',
        'size': 10,
        'bold': 1,
        'italic': 0,
        'underline': 0,
        'foreground': 0,
        'background': 0,
        'align': 'L',
        'text': '',
        'priority': 2,
        'multiline': False
    }
]


def create_pdf(which):

    recipetitle = recipe_table_dat[which][1]
    recipeid = recipe_table_dat[which][0]
    f = Template(format="Letter", elements=elements, title="Recipe Printout")
    print(f'Elements is a {type(elements)} structure')
    f.add_page()

    #we FILL some of the fields of the template with the information we want
    #note we access the elements treating the template instance as a "dict"

    f["header"] = f"Greg's cookbook - {recipetitle} - Recipe ID {recipeid}"
    f["title"] = recipetitle  # 'Mongolian Beef and Spring Onions'
    f["recipeimage"] = images_table_dat[which][2]
    f["description"] = recipe_table_dat[which][8]
    f["source"] = recipe_table_dat[which][2]
    f['servings'] = f'Servings: {recipe_table_dat[which][3]}'
    f['time'] = f'Total Time: {recipe_table_dat[which][4]}'
    f['rating'] = f'Rating: {recipe_table_dat[which][5]}'

    itms = len(ingredients_table_dat[which])
    ings = ''
    for itm in range(itms):
        ings = ings + ingredients_table_dat[which][itm][5] + "\n"
    f["ingredientshead"]
    f["ingredientitems"] = ings
    f["instructionhead"]
    f["instructions"] = instructions_table_dat[which][2]

    #and now we render the page
    filename = f'./{recipetitle}.pdf'
    f.render(filename)
    print(f'\n\n{"=" * 45}')
    print('        PDF has been generated')
    print('     Please open the PDF manually')
    print('=' * 45)
    print('\n\n')


def menu():
    print('Please select a recipe...')
    print('1 - Mongolian Beef and Spring Onions')
    print('2 - Amish White Bread')
    print('3 - "Crack" Chicken')
    resp = input('Please enter 1, 2, 3 or 0 to quit --> ')
    if resp == "0":
        print('Exiting program!')
        sys.exit(0)
    elif resp in ("1", "2", "3"):
        return resp
    else:
        return -1


def mainroutine():
    loop = True
    while loop:
        resp = menu()
        if resp == -1:
            print('Invalid selection.  Please try again')
        else:
            print(f'Requested recipe: {resp} \n')
            create_pdf(int(resp) - 1)


if __name__ == '__main__':
    mainroutine()