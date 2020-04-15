import operator
from string import digits
from collections import Counter
import re

# Variable to store the matching between the nucleotides #
NUCLEOTIDES = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}


class FileManipulator:

    # Function to read the given input txt file #
    def readSequence(self, fileName):
        file = open(fileName, "r")
        contents = file.readlines()             # Reading txt file line by line
        sequence = ""
        for line in contents:
            output = re.sub(r'(\d)+', '', line)  # Removing digits #
            output = re.sub(r'(\s)+', '', output)  # Removing whitespaces #
            sequence += output
        if sequence.find(":"):                  # If there's a ":" in our string; then we need to split and take the rest
            sequence = sequence.split(":")[1]
        return sequence

    # Function to write the sequence to another file ( testing purposes )
    def writeSequence(self, fileName, contents):
        file = open(fileName, "w")
        file.write(contents)
        file.close()

    # Function to convert given sequence to string #
    def convertSequenceToString(self, sequence):
        sequence = list(sequence)
        return sequence

class KMer:
    def __init__(self, string, reverse, stringFrequency, totalFrequency):
        self.string = string
        self.reverse = reverse
        self.stringFrequency = stringFrequency
        self.totalFrequency = totalFrequency


def findReverseComplimentOfKMer(kMer):
    return "".join([NUCLEOTIDES[kMer[i]] for i in range(len(kMer) - 1, -1, -1)])


def findListOfKMers(sequence, kValue):
    lengthOfSequence = len(sequence)
    listOfKMers = []
    for i in range(lengthOfSequence - kValue + 1):
        listOfKMers.append(sequence[i:i + kValue])
    #listOfKMers = [sequence[i:i + kValue] for i in range(lengthOfSequence - kValue + 1)]
    return listOfKMers


def findMostCommonKMers(sequence):
    kValue = 5                          # Initial kValue #
    lengthOfSequence = len(sequence)
    listOfMostCommonKMers = []                    # Dictionary to keep KMer instances #
    isEnd = False                       # Terminating condition #

    while not isEnd:
        listOfKMers = findListOfKMers(sequence, kValue)     # Extracting the list of kMers for a given kValue.
        frequenciesOfKMers = Counter(listOfKMers)           # Finding the frequencies of each kMers.
        mostCommonKMers = frequenciesOfKMers.most_common(5) # Fetch the 5 one that has the most frequency.

        for kMer in mostCommonKMers:                        # For each kMer; we'll find reverse comp and freqs.
            reverseCompliment = findReverseComplimentOfKMer(kMer[0])
            reverseFreq = sequence.count(reverseCompliment)
            kMerObject = KMer(kMer[0], reverseCompliment, kMer[1], reverseFreq)
            listOfMostCommonKMers.append(kMerObject)

        if max(frequenciesOfKMers.values()) == 1:           # If the maximum frequency equals 1; then we don't need to search more
            isEnd = True
        else:
            kValue += 1

    return listOfMostCommonKMers


def main():
    listOfFileNames = ["WUHAN.txt", "NEPAL.txt"]
    listOfFileNamesForFormatted = ["wuhanOutput.txt", "nepalOutput.txt"]
    fileManipulator = FileManipulator()

    for file in range(2):
        currentFile = listOfFileNames[file]
        currentSequence = fileManipulator.readSequence(currentFile)
        fileManipulator.writeSequence(listOfFileNamesForFormatted[file], currentSequence)
        kMersReturned = findMostCommonKMers(currentSequence)
        for kMer in kMersReturned:
            print(kMer.string + " : " + kMer.reverse + " : " + str(kMer.stringFrequency) + " : " + str(kMer.totalFrequency))

        print()
        print()
        print()


if __name__ == '__main__':
    main()
'''


def main():

    for i in range(2):

        print()
        print()
        print()
        print("THE MOST FREQUENT KMERS AND FREQUENCIES")
        for kMer in dictOfKMerFrequency:
            pureFrequency = dictOfKMerFrequency[kMer]
            reverseComp = findReverseCompOfKMer(kMer, NUCLEOTIDES)
            reverseFreq = currentSequence.count(reverseComp)
            totalFreq = pureFrequency + reverseFreq

            print(kMer + " : " + str(pureFrequency))
            print(kMer + " : " + str(totalFreq))
            print()


if __name__ == '__main__':
    main()
'''