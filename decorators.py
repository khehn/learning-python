#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:48:26 2019

@author: kevin

Cheatsheet
------------------------------
-   Decorators are higher-order functions, meaning they take another function as 
    input and extending their behavior, without modifying it
    
-   In python, functions are first-class objects. This means one can pass them
    around and use them as arguments
    
-   Since decorators are functions, you can use them like regular functions. 
    You could, for instance, put them into a module and import from there

-   What is introspection? -> Ability of an object to know about its own 
    attributes at runtime
    
-   If we use decoration, pythons introspection is loosing information, since
    the function now thinks, it is the wrapper function. Since this is not very
    useful, one can use functools
    
-   It is not only possible to decorate functions, but also classes
"""

###############################################################################
######################## Passing functions ####################################
###############################################################################

# Just a simple function
def add_one(number):
    return number + 1


# Interesting way to format a string!
def say_hello(name):
    return f"Hello {name}"

# Just another greeting function
def be_awesome(name):
    return f"You are awesome, {name}"

# This function takes another function as input
def greet_kevin(func):
    return func("Kevin")

# Hand over different functions to the greet_kevin function 
print(greet_kevin(say_hello))
print(greet_kevin(be_awesome))

###############################################################################
######################## Inner functions ######################################
###############################################################################

# Define a parent function
def parent(num):
    def first():
        return "Hi, I am the first inner function"
    
    def second():
        return "Hi, I am the second inner function"
    
    # Inner functions are not available outside their parent function.
    # Therefore we return one of them
    if num == 1:
        return first
    else:
        return second
    
first = parent(1)
second = parent(2)
print(first())
print(second())
    
    
###############################################################################
######################## Simple Decorators ####################################
###############################################################################

def my_decorator(func):
    def wrapper():
        print("Before the decorated function")
        func()
        print("After the decorated function")
    return wrapper

# Use the pie syntax for the decorations
@my_decorator
def say_wee():
    print("wee")

say_wee()


###############################################################################
######################## Decorators with arguments ############################
###############################################################################

def my_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello {name}")
    
greet("Kevin")


###############################################################################
######################## Return values from decorators ########################
###############################################################################

# If we do not explicitely return the value from the decorated function, 
# the result is lost
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    return f"Hello {name}"

print(greet("Kevin"))


###############################################################################
######################## Decorators and introspection #########################
###############################################################################

import functools
def my_decorator(func):
    # This decorator preservers the information about the wrapped function
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet_new(name):
    return f"Hello {name}"

# This statement shows, that the name is inherited from the wrapper method
print(greet.__name__)
# Now it is fixed and shows the information from the wrapper function
print(greet_new.__name__)


###############################################################################
######################## Using Decorators without wrapping ####################
###############################################################################

import random 
PLUGINS = dict()

# It is not always necessary to wrap the function in a decorator. We can also
# use them to register the functions
def register(func):
    PLUGINS[func.__name__] = func
    return func

@register
def say_hello(name):
    return f"Hello {name}"

@register
def greet(name):
    return f"Yo {name}"


def randomly_greet(name):
    greeter, func = random.choice(list(PLUGINS.items()))
    print(f"Using function: {func}")
    print(func(name))

randomly_greet("Kevin")


###############################################################################
######################## Decorators with arguments ############################
###############################################################################

def repeat(n_times):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n_times):
                func()
        return wrapper
    return my_decorator

@repeat(4)
def hello_world():
    print("Hello World")
    
hello_world()



