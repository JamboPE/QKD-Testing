import random
from tabulate import tabulate
import math

## Number of random bits
no_bits=input("Number of random bits: ")
valid=False
while valid == False: # Input validation
    try:
        no_bits=int(no_bits)
    except:
        no_bits=input("-----\nError: Value must be a number\nNumber of random bits: ")
    else:
        if no_bits <= 0:
            no_bits=input("-----\nError: Value must be above 0\nNumber of random bits: ")
        else:
            valid=True
print ("Number of random bits: "+str(no_bits)) # Print value for debugging or later reference

## Probability of an incorrect bit being received due to noise (error rate)
error_rate=input("Probability of an incorrect bit being received due to noise (error rate) [%]: ")
valid=False
while valid == False: # Input validation
    try:
        error_rate=int(error_rate)
    except:
        error_rate=input("-----\nError: Value must be a number\nProbability of an incorrect bit being received due to noise (error rate) [%]: ")
    else:
        if error_rate > 100 or error_rate < 0:
            error_rate=input("-----\nError: Value must be between 0 and 100\nProbability of an incorrect bit being received due to noise (error rate) [%]: ")
        else:
            valid=True
print ("Probability of an incorrect bit being received due to noise (error rate): "+str(error_rate)+"%") # Print value for debugging or later reference

def string_to_array(string): # Used for user display purposes to convert each character in a string to entries in an array
    array=[]
    for i in string: # iterate through each character in the string
        array.append(i) # append each character to the array
    return array

def array_to_string(array): # Used for user display purposes to convert each entry in an array to characters in a string
    string=""
    for i in array: # iterate through each entry in the array
        string = string + i # append each entry to the string
    return string

def generate_random_bits(length): # Used to generate a random array of 1s and 0s of a given length
    binary_string = ''.join(random.choice('01') for _ in range(length)) # generate a random string of 1s and 0s of a given length
    return string_to_array(binary_string) # Convert the string to an array and return it

def generate_random_bases(length): # Used to generate a random array of Ds and Rs of a given length
    bases_string = ''.join(random.choice('DR') for _ in range(length)) # generate a random string of Ds and Rs of a given length
    return string_to_array(bases_string) # Convert the string to an array and return it

def test_percentage(prob): # Essentially a coin flip with a given probability, has the given probability of returning true 
    # generate a random float between 0 and 1
    if random.random() < (prob/100): # if the float is less than the probability as a decimal, return true
        return True
    else: # otherwise, return false
        return False
    
def parity_sum(array): # Used to calculate the sum of all entries in an array
    total=0
    for i in array: # iterate through each entry in the array
        i = int(i)
        total=total+i # add each entry to the total
        if total == 2: # binary addition, so if the total is 2, set it to 0
            total=0
    return total

def split_array(array1, array2): # Used to split two arrays into two halves
    low_array1=[]
    up_array1=[]
    low_array2=[]
    up_array2=[]
    LB=0 # set the lower bound to 0
    UB=len(array1)-1 # set the upper bound to the length of the array minus 1
    mid=(LB+UB)//2 # find the middle index
    for i in range(0,len(array1)):
        if i <= mid:
            low_array1.append(array1[i])
            low_array2.append(array2[i])
        else:
            up_array1.append(array1[i])
            up_array2.append(array2[i])
    if len(up_array1) != len(up_array2) or len(low_array1) != len(low_array2) or parity_sum(low_array1) == parity_sum(low_array2) and parity_sum(up_array1) == parity_sum(up_array2):
        return "split_array() Error: The lengths of the arrays are not equal or the parity sums of the arrays are equal"
    elif parity_sum(low_array1) != parity_sum(low_array2) and parity_sum(up_array1) == parity_sum(up_array2):
        return [low_array1, low_array2, "low"]
    elif parity_sum(low_array1) == parity_sum(low_array2) and parity_sum(up_array1) != parity_sum(up_array2):
        return [up_array1, up_array2, "up"]
    else:
        return "Error"


bounds=[]
def cascade(correct_array, incorrect_array):
    global split_arrays
    split_arrays=[]
    global split_arrays2
    split_arrays2=[]
    global bounds
    bounds=[]
    while len(correct_array) != 1:
        both_arrays = split_array(correct_array, incorrect_array)
        correct_array = both_arrays[0]
        incorrect_array = both_arrays[1]
        if both_arrays[2] == "low":
            bounds.append("low")
        elif both_arrays[2] == "up":
            bounds.append("up")
        else:
            return "Error"
        print("lol",correct_array)
        split_arrays.append(produce_neat_array(incorrect_array, bounds, "Bob"))
        split_arrays2.append(produce_neat_array(correct_array, bounds, "Alice"))
    return(incorrect_array)

def produce_neat_array(array, bounds, person):
    if person == "Alice":
        neat_array = ["Alice"]
    if person == "Bob":
        neat_array = ["Bob"]
    length = no_bits
    for i in bounds:
        if i == "up":
            length = length - (length//2)
            for j in range(0,length):
                neat_array.append("")
        elif i == "low":
            length = length - (length//2)
    for i in array:
        neat_array.append(i)
    for i in range(0,no_bits-len(neat_array)):
        neat_array.append("")
    neat_array.append("")
    neat_array.append("")
    return neat_array

def h_func(p):
    #h = -1 * p * math.log2(p) - (1-p) * math.log2(1-p) # Shannon entropy
    h = (-1 * p * math.log2(p)) - ((1-p) * math.log2(1-p)) # Shannon entropy
    return h

## Alice's bits
alice_bits=["1","0","0","0","1","0","0","0","0","1"]#generate_random_bits(no_bits) # Generate Alice's random bits

## Bob's bits
bob_bits=[] # Initialise Bob's bits array
error_array=[] # Initialise error array for user display purposes
no_errors=0 
#for bit in alice_bits: # iterate through each bit in Alice's bits
#    if test_percentage(error_rate) == True: # if an error occurs in transmission, flip the bit
#            if bit == "1":
#                bob_bits.append("0")
#            elif bit == "0":
#                bob_bits.append("1")
#            else:
#                print("Error: alice bit is not 1 or 0") # Error message for debugging
#            error_array.append("X")
#            no_errors+=1
#    else: # otherwise, append the bit to Bob's bits array
#        bob_bits.append(bit)
#        error_array.append("")
bob_bits=["1","0","0","0","0","0","0","0","0","1"]
error_array=["","","","","X","","","","","",""]
no_errors=1
no_bits=len(alice_bits)
error_rate=no_errors/no_bits


def split_into_subblocks(string):
    print("No errors: "+str(no_errors))
    print("No bits: "+str(no_bits))
    substring_size = math.ceil(0.73/(no_errors/no_bits))
    print("Substring size: "+str(substring_size))
    no_subblock = math.ceil(no_bits / substring_size)
    subblock = 0
    bit = 0
    subblocks=[]
    for i in range(0,len(bob_bits)):
        if subblock == no_subblock and bit == 0:
                subblocks.append(string[i:])
        elif bit == 0 and subblock != no_subblock:
            subblocks.append(string[i:i+substring_size])
        elif bit == substring_size-1:
            bit = -1
            subblock += 1        
        bit += 1
    return subblocks
print(split_into_subblocks(bob_bits))
print(split_into_subblocks(alice_bits))

alice_parity, bob_parity = parity_sum(alice_bits), parity_sum(bob_bits) # Calculate the parity of Alice's and Bob's bits
if alice_parity == bob_parity: # If the parity of Alice's and Bob's bits are the same, do not use the cascade method
    print("Parity of Alice's bits: "+str(alice_parity)+"\nParity of Bob's bits: "+str(bob_parity)+"\nParity is the same, no cascade method required")
else:
    wrong_bit=cascade(alice_bits,bob_bits) # Otherwise, use the cascade method to find the error

# alice = alice string, bob = bob string, wrong_bit = index of wrong bit
def show_table(alice,a_parity,bob,b_parity,wrong_bit):
    print("\033[1m"+ "\033[4m" + "Error Correction - Cascade Protocol" + "\033[0m" + "\033[0m") # bold and underline table title
    # Add label to each array for tabulationIn QKD, Alice encodes a classical bit onto the polarization or phase of a photon and sends this photon to Bob. After repeating this step k times, Alice and Bob share two k-bit strings, and the crossover probability p of BSC is supposed as known. In public discussion, parity pair yk is transmitted via an authenticated classical channel. Therefore, we can obtain the following expression: 
    alice.insert(0,'Alice\'s bits')
    alice.append('Parity Value:')
    alice.append(a_parity)
    bob.insert(0,'Bob\'s bits')
    bob.append('Parity Value:')
    bob.append(bob_parity)
    error_array.insert(0, 'Error?')
    error_array.append('Total Errors:')
    error_array.append(no_errors)
    data = [alice,bob,error_array]
    for i in range(0,len(split_arrays)):
        data.append(split_arrays2[i])
        data.append(split_arrays[i])
    print(tabulate(data, tablefmt="simple_grid")) # Print table
    # Remove labels from each array so they can be used for further calculations
    #for array in data:
    #    if array == alice_bits or array == bob_bits or array == error_array:
    #        array.pop(0)
    #        array.pop(-1)
    #        array.pop(-1)
show_table(alice_bits,alice_parity,bob_bits,bob_parity,wrong_bit)
print("Error rate: "+str(no_errors/no_bits*100)+"%") # Print error rate
print("Parity bits:", len(split_arrays)*2) # Print number of parity bits
QBER =no_errors/no_bits # Calculate QBER
shannon_limit = h_func(QBER) # Calculate Shannon limit
print("Shannon Limit:", shannon_limit) # Print Shannon limit

# ^This is the Shannon limit for the cascade protocol - Most ideal case - ideal percentage of bits that would need to be given up as parity bits to correct the error
# Need to impliment a ratio (higher than 1) of the percentage of bits my cascade gives up commpared to the Shannon limit