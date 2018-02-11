"""
Word lists are from the English Open Word List, found at:
http://diginoodles.com/The_English_Open_Word_List_%28EOWL%29

this is probably suboptimal but I don't need to run it twice if it works once, so whatever
"""

import os

#switch this flag if you want to see the actual shift sets, as opposed to just knowing of their existence
show_sets = False

#generate all shifted versions of the word, including the word itself
def get_shifts(word):
    shifts = [word]

    for i in range(1, len(word)):
        #fun application of string slicing - look up what these do
        shifted_word = word[i:] + word[:i]
        shifts.append(shifted_word)

    return shifts

shift_sets = {}
complete_sets = {}

for word_list_filename in os.listdir("words"):
    #have to specify the encoding because there are some weird characters in there
    file = open("words/" + word_list_filename, "r", encoding="utf8")
    for word in file.read().splitlines():
        word_length = len(word)

        if word_length == 1: #trivial case, let's just skip it
            continue
        
        shifts = get_shifts(word)
        found_set = False

        #check to see if any shift of the word is present in the dictionary
        for shifted_word in shifts:
            if shifted_word in shift_sets:
                found_set = True
                shift_sets[shifted_word].append(word)

                #if this word completes the shift set, add the shift set to the completed sets
                if len(shift_sets[shifted_word]) == word_length:
                    #add it to the existing set of shift sets length n, or start that list if none exists
                    if word_length in complete_sets:
                        complete_sets[word_length].append(shift_sets[shifted_word])
                    else:
                        complete_sets[word_length] = [shift_sets[shifted_word]]

        #no existing set, start a new one keyed by this word
        if found_set == False:
            shift_sets[word] = [word]

print("Complete shift sets:")

#lets display these things in order
word_lengths = list(complete_sets.keys())
word_lengths.sort()

if show_sets:
    for word_length in word_lengths:
        print("Length " + str(word_length) + ":")
        for shift_set in complete_sets[word_length]:
            print(shift_set)
else:
    for word_length in word_lengths:
        print("Length " + str(word_length) + ": " + str(len(complete_sets[word_length])))
