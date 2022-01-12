# WordleSolver

An algorithm that can solve the word puzzle [Wordle](https://www.powerlanguage.co.uk/wordle/) with an optimal number of guesses on HARD mode.

## How to use the program

---

Copy this project with `git clone` and run `python3 solver.py` in the terminal.

When you run the program, the algorithm will provide you with an educated guess. Then, you type the guess into Wordle. Once you get the result of how many letters were right, you input it back into the program and will get another guess back. This process will continue until you have solved the puzzle!

Inputting the result of your guesses is easy. If a character is gray, enter '\_', if a character is yellow, enter the lowercase letter, and if a character is green, enter the uppercase letter. For example, if the program told you to guess "aeros" and the result of the guess was:

![image](1.png)

You would enter the result as: \_\_r\_\_

Here is another example:

![image](2.png)

You would enter the result as: DR_k\_

## How the algorithm works

Here's a quick run-down of how the algorithm works. We keep a list of words that the answer can be and keep removing from the list until only one word remains or we guess the right answer. Each word has a unique number associated with it. We can use this number to quickly determine if a word can be an answer based on the results of other guesses. If a word cannot be the answer, it will be removed from our list. The key to the accuracy and efficiency of this algorithm is how this unique number is generated.

The number is the product of a few prime numbers which lets us use modular arithmetic in a clever way! Each letter will have 6 prime numbers associated with it. One "yellow" number and five "green" numbers. We use the one yellow number when we know a letter is in the word but we don't know where. We use one of the green letters when we know that a letter is in a specific spot. You can see these prime numbers in [charDict.json](charDict.json). To actually calculate the number of a word, we multiply all the yellow numbers of the characters that make up the word together as well as certain green numbers. The green number we multiply depends on the position the letter appears. If the letter D appears in the first spot, we multiply by its 1st green number. If it was instead in the last spot of the word, we multiply by its 5th green number. The reason we do this is we can utilize modulo to check if a certain word can be an answer based on the result of another guess. For example, if we guessed "aeros" and the word we were trying to find was "drink", we will find that r is somewhere in the word but not in the third spot. Let us say a word has number n. If n%r's yellow number does not equal 0, then we know that word cannot be zero and we can remove it from the list. Also, if n%r's third green number equals 0, we know that it cannot be the answer because r cannot be in the third spot. Similar logic is applied when multiple letters are yellow or some letters come up green. The value of each word does not change, so we can process this information once and store it in a txt file to be used later which is what I did in wordList.txt! If you would like to use a different set of words than what I used, feel free to change the words.txt file and run `process.py` to generate a new wordList file.

## Optimizations

One way to make the algorithm take fewer guesses is to make smarter guesses. As such, an optimization I decided to make is to take into account letter frequency. Letters that appear more often have lower prime numbers associated with them and also that the word that is guessed always has the smallest number associated with it. Now, the primes associated with each letter aren't just chosen arbitrarily and actually tell us some information. "e" is the most common letter and as such has the six smallest prime numbers. I can sort the wordlist and make the algorithm guess the word with the smallest number. So, our algorithm is more likely to guess a word with "e" in it than "q" since words with "e" will probably be smaller. This is good because "e" is much more likely to be in the word than "q". Also, I only need to sort the list once in `process.py` so there is no significant performance hit!

A drawback of this approach is that words that are made up of repetitive common letters have very low values and are guessed much more. This is not good because words with repeating letters make it harder to narrow down our potential guesses! For example, consider the word "esses" which is made up of only of the two most common letters. It's good that our guesses consist of letters that are common but it is bad that we only get information about two different letters. The way I fixed this is by multiplying words that have characters repeated two or three times by a much bigger prime number so they are weighed down and guesses less often.

Another optimization I made is taking into account how common a word is. There are a lot of niche words in the list that are very rarely used which are likely not the answer to the puzzle. So, once I've narrowed down the possible words to less than a hundred, it makes sense to guess the more common words first. This is why I introduced a second number that is associated which each word. The second number is the frequency of a word in Wikipedia articles. Once there are less than 100 words in the list, the list is resorted by this second number rather than the first and so each guess will be the most common word remaining!

## Further Optimizations

As I mentioned before, one of the optimizations I made was having more common letters correspond with smaller prime numbers and sorting the list of words based on the number associated with each word. This is all done just once for each set of words in `process.py` and is very computationally efficient. However, if more accuracy is desired, the prime number associated with each letter can be re-generated after each guess because the frequency of each letter is likely to change. This may increase accuracy slightly but will take much longer to process which is why I opted against it. After each guess, I would have to re-check the frequency of each letter, calculate the value of each word, and then resort to the entire list based on this new value.

## Sources

- [Wordle](https://www.powerlanguage.co.uk/wordle/) is by [PowerLanguage](https://www.powerlanguage.co.uk/wordle/)
- List of 5 letter words is based on SOWPODS and was taken from [Word Game Dictionary](https://www.wordgamedictionary.com/sowpods/download/sowpods.txt). I suspect that PowerLanguage used the same source for wordle as he used a similar source for another project.
- The frequency of words was taken from [lexepedia](https://en.lexipedia.org/) with a minimum frequency of 1, length of 5, and only includes Wiktionary Words.
