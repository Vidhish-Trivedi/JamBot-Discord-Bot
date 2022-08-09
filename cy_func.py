# listing the english alphabet. 
list_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def coder(text, shift, direction):
    if (direction == "encode"):
        shift = shift
    elif (direction == "decode"):
        shift *= (-1)
    list_text = []
    for i in range(len(text)):
        list_text.append(text[i])
    for i in range(len(list_text)):
        for j in range(len(list_letters)): # shifting the letter.
            if list_text[i] == list_letters[j]:
                if (j + shift%26 < 26):
                    list_text[i] = list_letters[j + shift%26] 
                    # if not in range of list then do: (j + shift%26)[>=26] - 26.
                elif (j + shift%26 >= 26):
                    list_text[i] = list_letters[j + shift%26 - 26]
                break # letter is to be shifted only once.
    dir_str = f"{direction}d text is:" # printing the second print() without new line.
    txt = "".join(list_text) # printing list as a string.
    return([dir_str, txt])
    