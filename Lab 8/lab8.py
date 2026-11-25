## Question 1
def times(a,b): 
    # a*b = a + a*(b-1) + .... 
    if b == 1: 
        return a 

    return a + times(a, b-1) 

# time complexity: O(n) 
print(times(6,100))
"""
Call Tree :
times(a,b) -> times(a,b-1) -> times(a,b-2) -> ... -> times(a,1)
calls for at most b-1 times -> O(n) 
"""

## Question 2
def digit_sum(n): 
    ## n//10 removes the last digit, equals 0 if only a single digit is left. 
    if n//10 == 0: 
        return n
    return n%10 + digit_sum(n//10) #remove last digit 

print(digit_sum(123))

## Question 3
def remainder(a,b): 
    # Calculating a%b
    # consider that we can repeatedly call a - b for n times, that is what division is. If digit returned is negative, return last value. 

    if a < 0: 
        return a+b #return as remainder, step backwards one step

    return remainder(a-b, b) #step down by a-b 

print(remainder(7,2))

## Question 4 (Linear Search) 
def linearSearch(L,e): 
    #Consider that we can pass through the lower number of the list. 
    #The number of calls gives us the index. 

    if L[0] == e:
        return 0 

    return 1 + linearSearch(L[1:], e) #pass sublist 

print(linearSearch([5, 8, 2,9], 2))


## Question 5
def interLeave(L1,L2): 
    # Note that interleaving some list is akin to extending the interleaving of the ending: 
    if len(L1) == 1 and len(L2) == 1: #assume equal lengths
        print(len(L1))
        print([L1[0],L2[0]])
        return [L1[0], L2[0]]
    out = [L1[0], L2[0]]
    out.extend(interLeave(L1[1:], L2[1:]))
    return out

print(interLeave([1, 2, 3], ["a","b", "c"]))

## Question 6
def flipValues(L,start,end): 
    if start == end or end < start: 
        return None #stop executing
    L[start],L[end] = L[end],L[start]
    flipValues(L, start + 1, end -1)

def reverse_rec(L): 
    # Consider that for some list [a,b,c,d,e] -> [e,d,c,b,a]: 
    # we reverse 1, len(L)-1 
    flipValues(L, 0, len(L)-1)

L = [0,1,2,3,4]
reverse_rec(L) 
print(L) 

## Question 7

def middlePrint(L):
    # consider that for some list: 
    # [0 1 2 3 4 5 6] -> 3 2 4 1 5 0 6 
    # len = 7, len//2 = 3 
    mid = len(L)//2
    if len(L) == 0:
        print()
    elif len(L) == 1:
        print(L[0])
    else:
        print(L[mid], L[mid-1], end=" ")
        middlePrint(L[0:mid-1] + L[mid+1:len(L)])

A = [0, 1, 2, 3, 4, 5, 6]
middlePrint(A)

## Question 8
# Prompt Used: 
'''
I am a first-year engineering student learning recursion in Python.
Give me three practice problems on recursion, in increasing order
of difficulty, similar in style to these: computing x to the power
of n using only multiplication, summing the digits of a number,
and reversing a list in place using a helper function. The
solutions must not use loops. For each problem, give the function
signature and three test cases with their expected outputs. Do not
give me the solutions.
'''
### Used Gemini Auto: Respose: 
"""Here are three practice problems on recursion in Python, ordered from easiest to hardest, designed around foundational engineering problem-solving patterns without loops.

---

### Problem 1: Count Occurrences in a List
Write a recursive function that counts how many times a target value appears in a list of integers without using any loops.

**Function Signature:**
def count_occurrences(arr: list[int], target: int) -> int:

**Test Cases:**
* count_occurrences([3, 1, 4, 1, 5, 9, 1], 1) -> 3
* count_occurrences([10, 20, 30], 5) -> 0
* count_occurrences([], 7) -> 0

---

### Problem 2: Check If a String Is a Palindrome
Write a recursive function that returns True if a given string reads the same forwards and backwards, and False otherwise, without using loops or string slicing reversals ([::-1]).

**Function Signature:**
def is_palindrome(s: str) -> bool:

**Test Cases:**
* is_palindrome("racecar") -> True
* is_palindrome("engineering") -> False
* is_palindrome("a") -> True

---

### Problem 3: Flatten a Nested List
Write a recursive function that takes a nested list (where elements can be integers or other lists of integers, nested to arbitrary depth) and returns a single flat list of all integers in order, without using loops.

**Function Signature:**
def flatten_list(nested: list) -> list[int]:

**Test Cases:**
* flatten_list([1, [2, 3], [4, [5, 6]], 7]) -> [1, 2, 3, 4, 5, 6, 7]
* flatten_list([[1, [2]], [], [[[3]]]]) -> [1, 2, 3]
* flatten_list([]) -> []"""

## 8.1 

def counter(L,e,val=0): 
    count = val
    if len(L) == 0: 
        return val
    elif L[0] == e: 
        count += 1
    return counter(L[1:],e,count)
    
def count_occurrences(L,e): 
    return counter(L,e)

# passes all AI test cases
print(count_occurrences([3, 1, 4, 1, 5, 9, 1], 1)) #3
print(count_occurrences([10, 20, 30], 5)) #0
print(count_occurrences([], 7)) #0

# 8.2 
def is_palindrome_step(S,start,end): 
    # Given some word, some collection of strings, we can check palindromeness by checking the characters on the same index.
    # Checking if the same letter is being compared, or if we've passed. If we have and we haven't called False, return True. 
    if start >= end: 
        return True
    if S[end] == S[start]: #Checks if it's still the same
        return is_palindrome_step(S,start+1,end-1)
    else: # If not. return false.
        return False
    


def is_palindrome(S): 
    return is_palindrome_step(S,0,len(S)-1)

print(is_palindrome("racecar"))
print(is_palindrome("engineering"))
print(is_palindrome("a"))

# Question 9
def splitLists(L, elems): 
    out = [] 
    buffer = []
    for char in L: # iterate through list
        print(char)
        if char in elems: #if character is within elements
            out.append(buffer)
            buffer = []
        else: 
            buffer.append(char) 
    out.append(buffer)
        
    return out 

print(splitLists([1, 2, 6, 4, 5, 3, 7], [3, 6]))
