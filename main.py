import operator
from string import digits
from collections import Counter
import re

# Variable to store the matching between the nucleotides #
NUCLEOTIDES = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}


# Class is used to reading / writing operations to / from file
class FileManipulator:

    # Function to read the given input txt file #
    def readSequence(self, fileName):
        file = open(fileName, "r")
        contents = file.readlines()  # Reading txt file line by line
        sequence = ""
        for line in contents:
            output = re.sub(r'(\d)+', '', line)  # Removing digits #
            output = re.sub(r'(\s)+', '', output)  # Removing whitespaces #
            sequence += output
        if sequence.find(":"):  # If there's a ":" in our string; then we need to split and take the rest
            sequence = sequence.split(":")[1]
        return sequence

    # Function to write the sequence to another file #
    def writeSequence(self, fileName, contents):
        file = open(fileName, "a")
        file.write(contents)
        file.write("\n")
        file.close()

    # Function to clear the contents of the file #
    def clearFileContents(self, fileName):
        file = open(fileName, "w")
        file.truncate(0)
        file.close()

    # Function to convert given sequence to string #
    def convertSequenceToString(self, sequence):
        sequence = list(sequence)
        return sequence


# Class to represent the KMer objects #
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
    return listOfKMers


def checkTerminatingCondition(frequenciesOfKMers):
    if max(frequenciesOfKMers.values()) == 1:
        return True
    return False


def findMostCommonKMers(sequence):
    kValue = 5  # Initial kValue #
    listOfMostCommonKMers = []  # Dictionary to keep KMer instances #
    isEnd = False  # Terminating condition #

    while not isEnd:
        listOfKMers = findListOfKMers(sequence, kValue)  # Extracting the list of kMers for a given kValue.
        frequenciesOfKMers = Counter(listOfKMers)  # Finding the frequencies of each kMers.
        mostCommonKMers = frequenciesOfKMers.most_common(5)  # Fetch the 5 one that has the most frequency.

        if checkTerminatingCondition(frequenciesOfKMers):  # Checking if we should terminate or go on
            isEnd = True
        else:
            kValue += 1                             # If didn't terminate, then we need to inc kValue

        for kMer in mostCommonKMers:  # For each kMer; we'll find reverse comp and freqs.
            if kMer[1] == 1:
                break
            reverseCompliment = findReverseComplimentOfKMer(kMer[0])
            reverseFreq = sequence.count(reverseCompliment)
            kMerObject = KMer(kMer[0], reverseCompliment, kMer[1], reverseFreq)
            listOfMostCommonKMers.append(kMerObject)

    return listOfMostCommonKMers


def main():
    # Variables to be used #
    listOfFileNames = ["WUHAN.txt", "NEPAL.txt"]
    listOfFileNamesForFormatted = ["wuhanOutput.txt", "nepalOutput.txt"]
    fileManipulator = FileManipulator()

    # We need to process each file; so we have a loop in here #
    for file in range(2):
        fileManipulator.clearFileContents(listOfFileNamesForFormatted[file])    # Clearing the previous contents #
        fileManipulator.writeSequence(listOfFileNamesForFormatted[file], "KMer : Rev.Comp. : KMer Freq : Total Freq (KMer + Rev.Comp.)")
        currentFile = listOfFileNames[file]
        currentSequence = fileManipulator.readSequence(currentFile)
        kMersReturned = findMostCommonKMers(currentSequence)
        for kMer in kMersReturned:
            aboutToWrite = kMer.string + " : " + kMer.reverse + " : " + str(kMer.stringFrequency) + " : " + str(
                kMer.totalFrequency)
            fileManipulator.writeSequence(listOfFileNamesForFormatted[file], aboutToWrite)
        print()
        print()
        print()


if __name__ == '__main__':
    main()
