import os
import math
import json
import sys
import subprocess

# these values instead of 0/1 help the regression reach local optima faster
positive = 0.9 
negative = 0.1

# Read in all possible ingredients
Ingredients = []
with open('ingredients.txt') as ingredient_data:
    Ingredients = ingredient_data.readlines()
    MAX_INGREDIENTS = len(Ingredients)

# Dictionary for looking up column index of an ingredient
lookup = {}
for ingre in Ingredients:
    lookup[ingre] = Ingredients.index(ingre)

# Read in test data and format it 
with open('test_data_sample.json', 'r') as test_data:
    with open('script_files/test_data_sample.txt', 'a') as output:
        for r in test_data:                
            recipe = json.loads(r)
            id = recipe['id']
            ingredients = recipe['ingredients']
            line = str(id) + ', '
            l = [negative for x in range(0,MAX_INGREDIENTS)]
            for I in Ingredients:              # ~1,675 Max ingredients
                for i in ingredients:          # less than 15 on average
                    if I.replace('"','').strip() == i:
                        l[lookup[I]] = positive # constant time lookup
            line += str(l).replace('[','').replace(']','')
            line += '\n'
            output.write(line)

C = {}
f = sys.argv[1]
number_observations = 0
with open(f) as training_set:
    with open('script_files/data.csv', 'a') as training_data:
        # set up header row
        lin = 'cuisine'
        for ingr in Ingredients:
            lin += ', %s' % ('x' + str(lookup[ingr]))
        lin += '\n'
        training_data.write(lin)
        # fill in binary data
        for r in training_set:                      # ~800 recipes in sample file
            number_observations += 1
            recipe = json.loads(r)
            id = int(recipe['id'])
            cusine = recipe['cuisine']
            if cusine in C:
                C[cusine].append(id + 2)
            else:
                C[cusine] = [[], id + 2] # 1st spot reserved for test input values
            ingredients = recipe['ingredients']
            line = cusine + ', '
            l = [negative for x in range(0,MAX_INGREDIENTS)]
            for I in Ingredients:              # ~1,675 Max ingredients
                for i in ingredients:          # less than 15 on average
                    if I.replace('"','').strip() == i:
                        l[lookup[I]] = positive # constant time lookup
            line += str(l).replace('[','').replace(']','')
            line += '\n'
            training_data.write(line)

def prod(pair):
    # multiply coefficient by binary variable's value
    if pair[0].strip() == 'NA' or pair[0].strip() == 'NULL':
        return 0
    return float(pair[0])*float(pair[1])

def predict(value):
    # run value through sigmoid function
    try:
        return 1/(1+math.exp(-value))
    except OverflowError:
        return 0

for cuisine in C:
    with open('script_files/data.csv', 'r') as input_f, open('script_files/' + cuisine + '.csv', 'w') as output_f:
        l = input_f.readline()
        output_f.write(l)
        # cycle through cusines, write 1 for curr cusine and 0 for rest
        for line in input_f:
            if cuisine + ',' in line.replace('"','').strip():
                l = str(positive) + ',' + line.split(',', 1)[1]
                output_f.write(l)
            else:
                l = str(negative) + ',' + line.split(',', 1)[1]
                output_f.write(l)
    if number_observations / MAX_INGREDIENTS < 2: 
        included_vars = number_observations / 2 
    else: 
        included_vars = MAX_INGREDIENTS-1
    # run logit with R, get the coefient values from R output files
    command = 'Rscript'
    path = 'rscript.R'
    args = ['script_files/' + cuisine + '.csv', 'script_files/' + cuisine + '.txt', str(included_vars)]
    cmd = [command, path] + args
    process = subprocess.Popen(cmd, stdout=open(os.devnull, "w"))
    process.wait()
    with open('script_files/' + cuisine + '.txt') as output:
        intercept = float(output.readline())
        coefs = []
        for l in output:
            coefs.append(l)
        # open test file.txt and run formula for each line in file
        with open('script_files/test_data_sample.txt', 'r') as test_file:
            for line in test_file:
                test_input = line.split(', ')
                id = test_input[0]
                test_input = test_input[1:]
                formula = map(lambda pair: prod(pair), zip(coefs,test_input)) # magic
                value = intercept + sum(formula)
                prediction = predict(value)
                C[cuisine][0].append((id,prediction)) 
    # clean up uneeded files
    try:
        os.remove('script_files/' + cuisine + '.txt')
        os.remove('script_files/' + cuisine + '.csv')
    except OSError:
        pass
    print('fit ' + cuisine)
# clean up the rest of the files we created
try:
    os.remove('script_files/test_data_sample.txt')
    os.remove('script_files/data.csv')
except OSError:
    pass

# Find best fit for each test value by picking classification w/ highest predicted probability
best_fit = {}
for c in C:
    for id, xi in C[c][0]:
        if id not in best_fit:
            best_fit[id] = (c, xi)
        elif best_fit[id][1] < xi:
            best_fit[id] = (c, xi)
# write predictions to file
with open('recipes.csv', 'a') as f:
    for id in sorted(best_fit):
        f.write(id + ',' + best_fit[id][0] + '\n')

