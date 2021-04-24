from pprint import pprint
import csv
import string
import sre_yield
import time


# The function CrosswordsDictionary initializes the crossword as a dictionary where they keys are
# the number id of the word , and as an item an array containg the letters of the word .
def CrosswordsDictionary(filename,TempCrosswords):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lettersnumb=[]
            for i in range(0,len(row[1])):
                lettersnumb.append(row[1][i])
            TempCrosswords.update({int(row[0]):lettersnumb})

#The functions fills the 2-dimensional adjacent matrix [i][j]=x  where the word with the id i crosses the word with the
#id j  in j's x position of letters , if the value of x = -1 it means that i does not cross j and vice versa obviously .

def Intersections(filename,IntersectionMatrix):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for value in range(2,len(row),2):
                i=int(row[0])
                j=int(row[value])
                x=int(row[value+1])
                IntersectionMatrix[i][j]=x


#Whenever a word is added we call UpdateCrossword to update all the words it crosses with the letter that was added
#in the intersected position

def UpdateCrossword(updatedkey,CrossWordsdict):
    for j in range(0, len(IntersectionsMatrix)):
        if IntersectionsMatrix[updatedkey][j] !=-1:
            AffectedKey=j
            PositionToChange=IntersectionsMatrix[updatedkey][j]
            PositionToCopy=IntersectionsMatrix[j][updatedkey]
            ValueToCopy=CrossWordsdict[updatedkey][PositionToCopy]
            CrossWordsdict[AffectedKey][PositionToChange]=ValueToCopy


# To avoid duplicates words generated should be stored in sets
#The function stores the regular expressions in a dictionary where the expression is the key and the value is 0-1
# it has been used to fill a word or not.
def RegularExpressionsDictionary(filename,RegularExprDict):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            RegularExprDict.update({row[0]: 0})


#The following function checks if the word generated by the regular expressions could be fitted in
# the letters already placed by intersections if they exist and have been filled
# the inputs takes into account that the words generated are of the same length as the word they are trying
#to fill.

def ValidateWord(WordToBePlaced,PlacementPosition,CrosswordDict):
    IncompleteWord=CrosswordDict[PlacementPosition]
    for i in range(0,len(IncompleteWord)):
        if IncompleteWord[i]!="." and IncompleteWord[i] !=WordToBePlaced[i]:
            return False
    return True


# The following functions returns the key-id of the word that we will attempt to fill next
# the selection will


# Perharps when  fill a word we should place it a the bottom of the dict so the first time is
# comes upon a 1 meaning a completed word  from the (completed/total letters) we should break and
# save time.
def SelectWordToFill(CrosswordDict):
    SelectedKey=-1
    CompletionPercentage=-1
    for key in CrosswordDict:
        filled=0  # position in word already filled with a letter.
        word=CrosswordDict[key]
        for position in word:
            if position != ".":
               filled += 1
        if filled/len(word) > CompletionPercentage and filled/len(word) != 1:
            SelectedKey = key
            CompletionPercentage = filled/len(word)
    return SelectedKey


def SolveCrossword(CrosswordsInput,counter):
    # We locate an empty word with the strategy we chose , if the return is -1 it means it didnt find
    # and we have successfully filled the dictionary.
    EmptyWordKey=SelectWordToFill(CrosswordsInput)
    if EmptyWordKey == -1:
        print("Counts" , counter)
        return True
    # We check all the available regular expressions to see which one could possibly generate a word
    # that would fill the empty word that was selected.
    for RegularExpression in RegularExpressions:
        if RegularExpressions[RegularExpression] == 0:
            #We generate test words from unused regular expressions .
            TestWords = set(sre_yield.AllStrings(RegularExpression, max_count=5,charset=string.ascii_uppercase))

            # Sets to not show duplicates , following line to sort out words of a different length .
            TestWords = [word for word in TestWords if len(word) == len(CrosswordsInput[EmptyWordKey])]


            keepvalue = CrosswordsInput[EmptyWordKey]
            keepreg= RegularExpression
            #Checking if any of the generated words from a single re , fits my empty word .

            for CandidateWord in TestWords:
                if ValidateWord(CandidateWord,EmptyWordKey,CrosswordsInput):
                    counter += 1

                    CandidateWordasArray=[]
                    for letter in CandidateWord:
                        CandidateWordasArray.append(letter)

                    CrosswordsInput[EmptyWordKey]=CandidateWordasArray
                    UpdateCrossword(EmptyWordKey, CrosswordsInput)


                    RegularExpressions[RegularExpression]=1

                    if SolveCrossword(CrosswordsInput, counter):
                        return True

                #We need to remove the last word added ,
                #Make available the regular expressions it used .
                # remove the intersections it updated




                CrosswordsInput[EmptyWordKey] = keepvalue
                UpdateCrossword(EmptyWordKey,CrosswordsInput)



                RegularExpressions[keepreg] = 0
                pprint(CrosswordsInput)

    return False










start_time = time.time()

Crosswords={}
CrosswordsDictionary("films.csv",Crosswords)

NumberOfWords=len(Crosswords)
IntersectionsMatrix= [[-1 for i in range(NumberOfWords)] for j in range(NumberOfWords)]
Intersections("films.csv",IntersectionsMatrix)

RegularExpressions={}
RegularExpressionsDictionary("films.txt",RegularExpressions)

count=0
SolveCrossword(Crosswords,count)
pprint(Crosswords)




print("--- %s seconds ---" % (time.time() - start_time))