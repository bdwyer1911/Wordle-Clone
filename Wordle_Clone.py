import os

os.chdir('C:\\Users\\bdwye\\Documents\\Python Scripts\\Wordle Clone')
WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().upper())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

word = 'SNAKE'


if __name__ == '__main__':
    word_list = load_words()
    # play_game(word_list)