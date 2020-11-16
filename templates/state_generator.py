# state machine implementation via coroutine (no need for synchronization primitives)
from __future__ import generators
import sys

def math_gen(n): #iterative function is generator
    from math import sin #lazy import
    while 1:
        yield n
        n = abs(sin(n))*31
def step_one(n):
    global cargo
    int colcount
    for row in row:
        for column in columns:
            if M[row,column] == 1:
                Colcover = 1



# jump targets are independent of state
def jump_to(val):
    if 0 <= val < 10: return f"ONES"
    elif 10 <= val <20: return f"TENS"
    elif 20 <= val < 30: return f"TWENTIES"
    else: return f"OTHER INTERVAL"

# get targets are state-sensitive and map from iter to new state
def get_ones(iter):
    global cargo
    while 1:
        print("\nONES     State:  ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='ONES':
            print(f'@{cargo:.17f}    ',end="") #trailing comma continues evaluation
            cargo = next(iter)
        yield (jump_to(cargo),cargo)
# get targets are state-sensitive and map from iter to new state
def get_tens(iter):
    global cargo
    while 1:
        print("\nTENS     State:  ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='TENS':
            print(f'#{cargo:.17f}    ',end="") #trailing comma continues evaluation
            cargo = next(iter)
        yield (jump_to(cargo),cargo)
# get targets are state-sensitive and map from iter to new state
def get_twenties(iter):
    global cargo
    while 1:
        print("\nTWENTIES State:  ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='TWENTIES':
            print(f"*{cargo:.17f}    ",end="") #trailing comma continues evaluation
            cargo = next(iter)
        yield (jump_to(cargo),cargo)
# halting condition
def exit(iter):
    jump = input('\n\n[manual co-routine for jump?] ')
    print ("...Jumping into middle of ",jump.upper())
    yield (f'{jump.upper()}', next(iter))
    print ("\nExiting from exit()...")
    sys.exit()

def scheduler(gendct, start):
    global cargo
    coroutine = start
    while 1:
        (coroutine, cargo) = next(gendct[coroutine])
        if coroutine == '':
            print("special exit")
            sys.exit()

# Scheduler here implements the state machine and is generic
# requires a dictionary of generator objects that have been instantiated
# each generator runs and then returns a pair containing the desired next target along with cargo (parameter leared)
# note: there is no end state generator. generators are allowed to determine global halt independently via sys.exit()
#
# the iterator math_gen is designed so that the iterator function does not need to manage past states, or pass values backwards and issues an indefinite stream.
# this convention is crucial in isolating the state transition function. 
if __name__ == "__main__":
    #initial value
    num_stream = math_gen(1)
    cargo = next(num_stream) # computes math_gen again 
    # predefined states, each with transition function operating on shared stream.
    # in the munkres algorithm they are operating on 
    gendct = {'ONES'        : get_ones(num_stream),
              'TENS'        : get_tens(num_stream),
              'TWENTIES'    : get_twenties(num_stream),
              'OTHER INTERVAL': exit(num_stream)         }
    scheduler(gendct, jump_to(cargo))
