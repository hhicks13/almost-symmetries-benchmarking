# state machine implementation via coroutine (no need for synchronization primitives)
from __future__ import generators
import sys

def math_gen(n): #iterative function is generator
    from math import sin #lazy import
    while 1:
        yield n
        n = abs(sin(n))*31
        
# jump targets are independent of state
def jump_to(val):
    if 0<= val < 10: return 'ONES'
    elif 10 <= val <20: return 'TENS'
    elif 20 <= val < 30: return 'TWENTIES'
    else: return 'OTHER INTERVAL'

# get targets are state-sensitive and map from iter to new state
def get_ones(iter):
    global cargo
    while 1:
        print("\nONES State:    ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='ONES':
            print("{}".format(cargo),end="") #trailing comma continues evaluation
            cargo = iter.next()
            yield (jump_to(cargo),cargo)
# get targets are state-sensitive and map from iter to new state
def get_tens(iter):
    global cargo
    while 1:
        print("\nTENS State:    ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='TENS':
            print("{}".format(cargo),end="") #trailing comma continues evaluation
            cargo = iter.next()
            yield (jump_to(cargo),cargo)
# get targets are state-sensitive and map from iter to new state
def get_twenties(iter):
    global cargo
    while 1:
        print("\nTWENTIES State:    ",end="") #trailing comma continues evaluation
        while jump_to(cargo)=='TWENTIES':
            print("{}".format(cargo),end="") #trailing comma continues evaluation
            cargo = iter.next()
            yield (jump_to(cargo),cargo)
# halting condition
def exit(iter):
    jump = raw_input('\n\n[co-routine for jump?] ').upper()
    print ("...Jumping into middle of ",jump,end="")
    yield (jump, iter.next())
    print ("\nExiting from exit()...",end="")
    sys.exit()

def scheduler(gendct, start):
    global cargo
    coroutine = start
    while 1:
        (coroutine, cargo) = gendct[coroutine].next()

# Scheduler here implements the state machine and is generic
# requires a dictionary of generator objects that have been instantiated
# each generator runs and then returns a pair containing the desired next target along with cargo (parameter leared)
# note: there is no end state generator. generators are allowed to determine global halt independently via sys.exit()
#
# the iterator math_gen is designed so that the iterator function does not need to manage past states, or pass values backwards and issues an indefinite stream.
# this convention is crucial in isolating the state transition function. 
if __name__ == "__main__":
    num_stream = math_gen(1)
    cargo = num_stream.next()
    gendct = {'ONES'        : get_ones(num_stream),
              'TENS'        : get_tens(num_stream),
              'TWENTIES'    : get_twenties(num_stream),
              'OUT_OF_RANGE': exit(num_stream)         }
    scheduler(gendct, jump_to(cargo))
