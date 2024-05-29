import os
import random
from rich.console import Console
from rich.theme import Theme
from string import ascii_letters, ascii_uppercase 
from collections import Counter

#start by changing the working directory bc I'm a noob with VScode and don't know how to do it besides this way
os.chdir('C:\\Users\\bdwye\\Documents\\Python Scripts\\Wordle Clone')

#define our text file that contains the list of all words
WORDLIST_FILENAME = "words.txt"

#initialize our rich console
console = Console(width=40)

#function that refreshes the console and adds a header
def refresh_page(headline):
    '''
    Refreshes our console
    '''
    console.clear()
    console.rule(f"[bold blue]:muscle: {headline} :muscle:[/]\n")

#get our list of words of specified length
def get_words(length):
    """
    Returns a list of words of the specified length
    """

    inFile = open(WORDLIST_FILENAME, 'r')
    
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().upper())
    
    correctLength = [word for word in wordlist if len(word) == length]
    return correctLength


def compare_words(guess,word):
    '''
    Compares two strings of equal length
    Returns an output in list form where 'X' indicates a letter in the right spot, 'O' indicates right letter
        in wrong spot, and '-' indicates an incorrect guessed letter
    '''

    #initialize our output list of placeholders
    output = ['-'] * len(word)

    #start by searching for if the letter is correct
    for index, (letter, correct) in enumerate(zip(guess, word)):
        if letter == correct:
            #assign an X to the output list to indicate a letter in the correct spot
            output[index] = 'X'

            #'check off' the letter in the correct word by removing it so it doesn't get marked again
            word = word.replace(letter,'-',1)
    
    #now find our letters that are in the word but in the wrong spot
    for index, (letter, correct) in enumerate(zip(guess, word)):
        #check if the letter is in the word and that it wasn't already found to be in the right spot
        if letter in word and output[index] == '-':
            #assign an O to the output list to indicate the letter is in the word but in the wrong spot
            output[index] = 'O'

            #'check off' the letter in the correct word by removing it so it doesn't get marked again
            word = word.replace(letter,'-',1)
    
    #return our list so we can style accordingly
    return output

def show_guesses(guesses, word):
    '''
    Show the guesses to the user in the console
    '''

    #initialize some empty lists for the letters
    green_letters = []
    yellow_letters = []
    gray_letters = []


    for guess in guesses:
        styled = []
        output = compare_words(guess,word)
        for checker, letter in zip(output, guess):
            #if we see an X, the letter should show up green to indicate it's correct
            if checker == 'X':
                style = 'bold white on green'
                green_letters.append(letter) #add to our list of correct letters

            #if it's an O, color it yellow 
            elif checker == 'O':
                style = 'bold white on yellow'
                yellow_letters.append(letter) #add to our list of correct letters in wrong spot
            
            #if it's not in the word, it should be white
            elif letter in ascii_letters:
                style = 'white on #666666'
                if letter not in green_letters and letter not in yellow_letters:
                    gray_letters.append(letter) #add to our list of guesses letters that aren't in word
            else:
                style = 'dim'

            #add the letter and it's proper style to our list
            styled.append(f"[{style}]{letter}[/]")
        
        #print out the guesses
        console.print("".join(styled), justify="center")
    
    #add some spacing
    print('\n')
        
    #now let's show the entire alphabet with the appropriate colors    
    styled = []
    allLetters = ascii_uppercase
    for char in allLetters:
        if char in yellow_letters:
            style = 'bold white on yellow'
        if char in green_letters: #green after yellow so that if a letter is in both lists it overrides and shows up green
            style = 'bold white on green'
        if char in gray_letters: #guessed and incorrect
            style = 'bold white on black'
        if char not in yellow_letters and char not in green_letters and char not in gray_letters: #these are the letters that haven't been guesses
            style = 'white on #666666'
        styled.append(f"[{style}] {char}")
    
    #print to console
    console.print(" ".join(styled), justify="center")


    
def game_over(word):
    '''
    Shows up if the user runs out of guesses to display the word
    '''
    print(f'The word was: {word}')


def main():

    #start by letting the user select the length of the word
    while True:
        try:
            # word_length = 5
            word_length = int(input('How many letters in the word would you like? '))
            break
        except ValueError:
            print("That's not an integer! Let's try again...")
            continue
    
    #get list of all words of that length
    validWords = get_words(word_length)

    #select our word from the lsit randomly
    word = random.choice(validWords)
    
    #initialize our guesses
    guesses = ['_' * word_length] * 6
    
    #thise code runs the game
    for guessID in range(6):
        refresh_page(headline=f"Guess {guessID + 1}") #refresh our header
        show_guesses(guesses, word) #show all the gueses
        validWord = False
        notGuessed = False

        #make sure the guess is a valid word, which also checks the input is the right length
        while not validWord:
            guesses[guessID] = input(f'\nGuess {guessID+1}: ').upper()
            if guesses[guessID] not in validWords:
                print("That's not a valid word. Try again")
                continue
            if guesses[guessID] in guesses[:guessID]:
                print("You've already guessed that word. Try again")
                continue
            validWord = True

        #if they guess the right word
        if guesses[guessID] == word:
            refresh_page(headline=f"Guess {guessID + 1}")
            show_guesses(guesses, word)
            print('Congratulations! You guessed the correct word')
            break

    #using a for-else here that only runs if the for loop isn't broken. This is for if they lose
    else:
        refresh_page(headline=f"GAME OVER")
        show_guesses(guesses, word)
        game_over(word)

if __name__ == '__main__':
    main()
    
