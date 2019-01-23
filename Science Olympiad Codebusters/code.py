# Codebusters code encrypter/decrypter 
# Oliver Tsang (oortsang~at~uchicago.edu) at UChicago Science Olympiad (2019)
#
#
# There are a bunch of helper functions, but here are the main ones:
#   1. affine(input, a, b)
#       Notes: caesar(input, shift) and atbash(input) are special cases
#   2. vigenere(input, keyword)
#       Note: If the keyword is as long as the input, you just have a running key cipher
#   3. aristocrats(input, permutation)
#       Note: the permutation is expected as an array of numbers from 0 to 25.
#       The number of the letter to replace 'a' with should go in the 0th position.
#       e.g., if you want to replace 'a' with 'h' and 'b' with 'a', the array would start [7, 0, ...]
#   4. hill(input, matrix)
#       Note: may be numerically unstable... use with caution!
# All of these come with an anti-function that takes in the same key and applies it in reverse.
# (antiaffine, anticaesar, antiatbash, antivigenere, antiaristocrats, and antihill)
#
# Make sure your computer has numpy installed!
# Easiest way to run: "python -i code.py" or "python3 -i code.py" depending on your installation of python
#
# Hopes for the future:
# - RSA key generation + encryption/decryption
# - Maybe machine cryptanalysis for aristocrats or one of the simpler ciphers
# 
# Cheers!

import numpy as np

def get_num(c):
    #can enter "get_num.__doc__" into the console for this help comment
    """ The number is 0-indexed.
    Returns whether the character was alphabetic, upper case, and then the number
    This helps preserve formatting. 
    Ex: get_num('a') = (True, False, 97)
    """
    res = ord(c)
    is_alpha = c.isalpha()
    is_upper = c.isupper()
    if is_upper:
        res = ord(c)- ord('A')
    elif is_alpha and not is_upper:
        res = ord(c) - ord('a')
    return (is_alpha, is_upper, res)
    
def get_char(is_alpha, is_upper, num):
    """Pass back the same stuff from get_num to get a character again."""
    if not is_alpha:
        return chr(num)
    elif is_upper:
        return chr(num + ord('A'))
    else:
        return chr(num + ord('a'))
    
def minv_26(a):
    """Gets the inverse of the number base 26"""
    if (a % 2== 0 or a % 13 ==0):
        print("smh %d has no inverse modulo 26" % a)
        return None
    else:
        a = a % 26
        minvs = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}
        return minvs[a]

def letter_counts(text):
    """ Counts up alphabetical letters """
    freqs = [0]*26
    for c in text:
        if c.isalpha():
            continue
        freqs[ord(c.lower())-ord('a')] += 1
    return freqs

def affine(input, a=1, b=0):
    """a should never be even or 13"""
    output = ""
    for c in input:
        is_alpha, is_upper, n = get_num(c)
        if is_alpha:
            n = (a*n+b) % 26
        output += get_char(is_alpha, is_upper, n)
    return output
    
def antiaffine(input, a=1, b=0):
    """a should never be even or 13"""
    output = ""
    ainv = minv_26(a)
    for c in input:
        is_alpha, is_upper, n = get_num(c)
        if is_alpha:
            n = (ainv*(n-b)) % 26
        output += get_char(is_alpha, is_upper, n)
    return output 

caesar = lambda input, shift: affine(input = input, a = 1, b = shift)
anticaesar = lambda input, shift: affine(input = input, a = 1, b = -shift)
atbash = lambda input: affine(input = input, a = -1, b = -1)
antiatbash = atbash #provided for convenience but also that's the whole idea of atbash

def vigenere(input, code):
    codelen = len(code)
    output = ""
    i = 0
    for c in input:
        is_alpha, is_upper, n = get_num(c)
        if is_alpha:
            n = (n + get_num(code[i % codelen])[2]) % 26
            i += 1
        output += get_char(is_alpha, is_upper, n)
    return output

antivigenere = lambda input, code: vigenere(input, affine(code, -1,0))    

def aristocrats(input, perm):
    """ Give a permutation of [0, ..., 25]
    Example: if you want 'a' to turn into 'h' then set the first element to 7
    and if you want to set 'b' to 'a', then set the second element to 0
    You can make a random permutation with: np.random.permutation(range(26)).
    """
    output = ""
    for c in input:
        is_alpha, is_upper, n = get_num(c)
        if is_alpha:
            n = perm[n]
        output += get_char(is_alpha, is_upper, n)
    return output

antiaristocrats = lambda input, perm: aristocrats(input, np.argsort(perm)) #inverse permutation
    
def hill(input, mat):
    """Pass in text and an invertible square matrix. Only works in base 26 right now! Sorry for base 29 folks!"""
    mat = mat.astype(np.int32)
    if np.math.gcd(int(np.round(np.linalg.det(mat))), 26) != 1:
        print("Matrix invalid for Hill Cipher! Not invertible modulo 26 - check the determinant")
        return None
    else:
        print("Input matrix size: %d x %d" % mat.shape)
    alphas = []
    uppers = [] #remember which letters were in upper case
    ns = []
    output = []
    a_tail_len=0 #number of 'a's added to the end of the string -- remove at the end
    d = mat.shape[0] #dimension of the square matrix
    input_len = len(input)
    print("Input string length: ", input_len)
    #put just the essentials into the ns array
    for i, c in enumerate(input): #iterate character by character
        is_alpha, is_upper, n = get_num(c)
        alphas.append(is_alpha)
        uppers.append(is_upper)
        if is_alpha:
            ns.append((n,i))
    #extend if necessary
    if len(ns) % d == 0:
        pass
    else:
        #append 'a' as necessary to the tail
        a_tail_len = (d - (input_len % d))
        ns += [(0, i) for i in range(len(ns), len(ns)+a_tail_len)]
        alphas += [True] * a_tail_len
        uppers += [False] * a_tail_len
        print("Message extended by %d characters" % (d - (input_len % d)))
    input_len = len(ns) #sanitized
    col_count = input_len//d #should be just the same as regular division
    ns = np.array(ns, dtype = np.int32) #for nicer notation
    #convert and store
    for i in range(col_count):
        curr_col = np.array(ns[d*i: d*(i+1), 0], dtype = np.int32)
        out_col = np.dot(mat, curr_col) % 26
        #print("Curr col:", curr_col, "out col:", out_col)
        for j in range(d):
            pos = ns[d*i+j, 1]
            letter = get_char(alphas[pos], uppers[pos], out_col[j])
            output.append(letter)
    #reformat to look pretty
    out_string = ""
    k=0 #use to count ns again
    for i in range(len(alphas)-a_tail_len):
        if alphas[i]:
            out_string += output[k]
            k += 1
        else:
            out_string += input[i]
    if (a_tail_len != 0):
        print("Implicitly appended", a_tail_len, " 'a's to the end of your string and cut them out. "
        "This may affect the encoded values of the last couple letters in the message.")
    return out_string

def mat_inv(mat):
    """Only inverts in base 26"""
    reg_det = np.linalg.det(mat)
    if np.isclose(reg_det, np.round(reg_det)):
        minv_det = minv_26(np.int(np.round(reg_det)))
    else:
        print("Yikes! An error occurred while trying to take the determinant of your matrix!")
        return None
    reg_inv = np.linalg.inv(mat)
    out = (reg_inv *reg_det* minv_det)
    vint = np.vectorize(lambda x: np.int(np.round(x)))
    if np.all(np.isclose(out, np.round(out), rtol=1e-6, atol=1e-8)):
        print(vint(out) %26)
        return vint(out) % 26
    else:
        print("Oops, we have some numerical accuracy issues while inverting the matrix! Please be careful.")
        print("Here is what we got before rounding:", out)
        #maybe don't return if it's too far?
        return out
antihill = lambda input, m: hill(input, mat_inv(m))

ma = np.array([(1,2,3),(3,7,5),(0,-1,11)], dtype = np.int64)
identity = np.array([[1,0,0],[0,1,0],[0,0,1]], dtype = np.int64)