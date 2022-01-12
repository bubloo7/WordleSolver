import json

allwords = open('wordList.txt', 'r').read().splitlines()

wordList = []
for word in allwords:
    split = word.split(',')
    wordList.append((int(split[0]), split[2], int(split[1])))

charDict = json.load(open('charDict.json'))

order = []
while(len(wordList) > 1):
    num = 1
    no = []
    val, guess, f = wordList[0]
    print("narrowed down to: " + str(len(wordList)) + " words")
    input("guess: " + guess)
    freqs = {}
    for c in guess:
        if c not in freqs:
            freqs[c] = 0
        freqs[c] += 1
    s = input("What was the result?\n")
    for i in range(len(s)):
        c = s[i]
        if c.isupper():
            c = c.lower()
            num *= charDict[c]['green'][i] * charDict[c]['yellow']
    for i in range(len(s)):
        c = s[i]
        if c == '_':
            c = guess[i]
            no.append(charDict[c]['green'][i])
            count = 1
            temp = num
            while(True):
                if temp % charDict[c]['yellow'] == 0:
                    count += 1
                    temp = temp/charDict[c]['yellow']
                else:
                    break
            no.append(charDict[c]['yellow']**count)
        
        elif c.islower():
            num *= charDict[c]['yellow']
            no.append(charDict[c]['green'][i])

    # print(num)
    # print(no)
    for i in range(len(wordList)-1, -1, -1):
        val, guess,freq  = wordList[i]
        if val % num != 0:
            wordList.pop(i)
            continue
        for n in no:
            if val % n == 0:
                wordList.pop(i)
                break
    
    if (len(wordList) < 100):
            wordList.sort(key = lambda x: x[2], reverse = True) 


print("answer is " + wordList[0][1])
