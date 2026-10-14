## How do we represent related information?

# We can represent related information using parallel lists

# Write a function that takes in two lists, one representing kids and one representing their favourite candies, as well as a string representing a kid's name
# The function should return that kid's favourite candy
# We're getting into the Halloween spirit early :)

kids = ["Anna", "Barb", "Carl"]
candies = ["KitKat", "Smarties", "Chocolate"]

def fave_candy_for_kid(kids, candies, kid):
    for i in range(len(kids)):
        if kids[i] == kid:
            return candies[i]

print(fave_candy_for_kid(kids, candies, "Carl"))

# When we have associated information, dictionaries can be a good way to store them

fave_candies = {"Anna": "KitKat", "Barb": "Smarties", "Carl":"Chocolate"}

# We can print this dictionary
print(fave_candies)

# To access a value within the dictionary, we just need the associated key
print(fave_candies["Barb"])

# We can rewrite the function to use a dictionary instead
def fave_candy_for_kid_dictionary(fave_candies, kid):
    return fave_candies[kid]

print(fave_candy_for_kid_dictionary(fave_candies, "Carl"))

## Grades

# Let's define a new dictionary, grades.


# We can modify existing values like this:


# We can also add entries, like this:


# Note that this is not similar to what can be done with lists: if an index does not exist in a list, we cannot add a value at that index:



# We don't have to have all the values (or all the keys) be the same type. For example, we can go



## Valid keys
# Keys in a dictionary have to be immutable. The following doesn't work:




# Why not?

## Keys, values and items
# We can set up a dictionary to store some of this year's nobel prize winners



# We can add more winners


# Let's get the list of all the keys in a dictionary:



# All the values:




# Note that the keys and the values are given in no particular order. We can go through all the keys, and all the values, using for-loops:





# We can go through all of the values



# You can also get the items in a dictionary -- those are the key-value pairs, as tuples:




## Iterating through a dictionary
# We can iterate through the keys, as we saw above:




# We can also iterate through the items:






## Solving dictionary problems with iteration
# How many nobel prize winners were there in each category this year?

def print_winners_by_prize(data):
    pass

## Removing items from the dictionary
# We can remove items from dictionaries using the del operator.

grades = {"PHY": "A+", "CIV": "A", "CSC": "A+", "ESC":"B+"}

# Suppose we want to remove the entry with the key "PHY". This is done similarly to removing elements from lists by specifying elements at what index we want to remove:



# We can also remove all the entries at ones:




# Let's restore the grades to what they were, and try to remove some of the entries according to their values (note that there's no easy way to do this -- del only removes entries using their keys.

grades = {"PHY": "A+", "CIV": "A", "CSC": "A+", "ESC":"B+"}
def correct_transcript_bad(grades):
    pass

correct_transcript_bad(grades)

# This first version we write will produce "RuntimeError: dictionary changed size during iteration"
# The reason we get an error is that, just like with lists, we cannot iterate over dictionaries while modifying their contents.

# Here is how to avoid the error: create a list of all the keys in the dictionary (that will from there on be independent of the dictionary), and go over all the keys, deleting the entries corresponding to them one-by-one.

def remove_bad_grades(grades):
    pass

remove_bad_grades(grades)
print(grades)

## Inverting a dictionary
grades = {"CSC": "A", "PHY": "B+", "MAT":"A+", "ESC":"A+"}
# Our goal is to create the following list:
# inv_grades = {"A": ["CSC"], "B+": ["PHY"], "A+":["MAT", "ESC"]}
def get_inv_grades(grades):
    pass

inv_grades = get_inv_grades(grades)
print(inv_grades)

## A festive counting problem (MT2023, Q6)
# Write a function that finds the element that occurs the most frequently in a given list of strings.
# For example, most_frequent_fave(["candy", "costumes", "midterms", "candy"]) should return "candy", since "candy" appears twice in the list of strings, which is more than any other string in the list.
# Assume there are no “ties”. You may not import any modules (like in other questions), but may otherwise use any functionality available in Python. You may use helper functions.
# Hint: one way (but not the only way) to start solving this problem is to count how many times "candy" appears and check if it appears more times than any other string in the list, etc.

def most_frequent_fave(faves):
    pass

print(most_frequent_fave(["candy", "costumes", "midterms", "candy"]))
