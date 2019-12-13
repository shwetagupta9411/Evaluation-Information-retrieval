"""
Runs part 2 of assignment.

python3 quesTwo.py
Args:
    -i inputFile.txt
    -w engineWeightsFile.txt
    -o ouputFile.txt
"""


import os
import sys, getopt
import string, time
from datetime import datetime

# To run the script -
# python3 quesTwo.py -i inputQuesTwo.txt -w inputTwoQuesTwo.txt -o outputFileTwo.txt

class EvaluationModel(object):
    def __init__(self, iFile, weightFile, oFile):
        self.iFile = iFile
        self.weightFile = weightFile
        self.oFile = oFile
        pass

    def evaluation(self):
        """
        This function applies-
        1. Interleaving
        2. CombSUM
        3. LCM
        And produces top 100 documents for each fusion technique.
        """
        try:
            outFile = open(self.oFile, "w")
            # storing the data in dataStructure (dictionary)
            with open(self.iFile) as f:
                dataStructure = {}
                fusedInterleaving = []
                for line in f:
                    row = line.split("\t") #splitting it by tab to get the next engines data
                    for r in row:
                        record = r.split(";") #splitting it by ; to get the doc value, rating and system
                        if record[0].strip().upper() in dataStructure.keys():
                            dataStructure[record[0].strip().upper()][record[1].strip()] = float(record[2].strip())
                        else:
                            dataStructure[record[0].strip().upper()] = {}
                            dataStructure[record[0].strip().upper()][record[1].strip()] = float(record[2].strip())

            """Interleaving"""
            #creating fusion list of documents for Interleaving
            count = 0
            while count < 100: #selecting top 100 documents
                for k in dataStructure.keys():
                    docList = list(dataStructure[k].keys()) #document list of every system
                    index = 0
                    while True:
                        if index < len(docList):
                            if docList[index] in fusedInterleaving: # if document is already present in the fusion list then taking the next element from that system
                                index = index + 1
                            elif count == 100:
                                break
                            else:
                                fusedInterleaving.append(docList[index])
                                count = count + 1
                                break
                        else:
                            count = count + 1
                            break


            # printing and writing the results in the file
            outFile.write("Top 100 results from Interleaving:\n")
            outFile.write("Rank \t Documents\n")
            print("\nTop 100 results from Interleaving:")
            print("Rank \t Documents")
            for i, doc in enumerate(fusedInterleaving[0:100],1):
                outFile.write("%d \t\t %s\n" % (i,doc))
                print("%d \t %s" % (i,doc))

            """CombSUM"""
            #normalizing the ratings
            for key in dataStructure:
                minimum = float(min(list(dataStructure[key].values()))) #minimum rating among all the ratings
                maximum = float(max(list(dataStructure[key].values()))) #maximum rating among all the ratings
                for normDoc in dataStructure[key].keys():
                    dataStructure[key][normDoc] = round(float((dataStructure[key][normDoc] - minimum)/(maximum-minimum)),2)


            comSumRes = self.fuseDocuments(dataStructure) #returns fused list of documents
            # printing and writing the results in the file
            outFile.write("\nTop 100 results from CombSUM:\n")
            outFile.write("Rank \t Documents \t Rating\n")
            print("\nTop 100 results from CombSUM:")
            print("Rank \t Documents \t Rating")
            for i, docSum in enumerate(comSumRes[0:100],1):
                outFile.write("%d \t\t\t %s \t\t\t %s\n" % (i, docSum[0], docSum[1]))
                print("%d \t %s \t\t %s" % (i,docSum[0],docSum[1]))

            """LCM"""
            engineWeight = self.getEngineWeight(self.weightFile) #returns engine and their weight
            # multiplying normalized ratings with engine weight
            for el in dataStructure.keys():
                for val in dataStructure[el].keys():
                    dataStructure[el][val] = round(float(dataStructure[el][val] * engineWeight[el]), 2)


            lcmRes = self.fuseDocuments(dataStructure) #returns fused list of documents
            # printing and writing the results in the file
            outFile.write("\nTop 100 results from LCM:\n")
            outFile.write("Rank \t Documents \t Rating\n")
            print("\nTop 100 results from LCM:")
            print("Rank \t Documents \t Rating")
            for i, docLCM in enumerate(lcmRes[0:100],1):
                outFile.write("%d \t\t\t %s \t\t\t %s\n" % (i, docLCM[0], docLCM[1]))
                print("%d \t %s \t\t %s" % (i, docLCM[0], docLCM[1]))

            outFile.close()
        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

    def fuseDocuments(self, dataStructure):
        """ This function applies the fusion among all systems documents """
        fusedCombSUM = {}
        for kComSum in dataStructure.keys():
            docListCombSUM = list(dataStructure[kComSum].keys())

            # adding the same documents rating from different systems and creating map of it.
            for docCombSum in docListCombSUM:
                if docCombSum in fusedCombSUM.keys():
                    fusedCombSUM[docCombSum] = round(float(fusedCombSUM[docCombSum] + dataStructure[kComSum][docCombSum]),2)
                else:
                    fusedCombSUM[docCombSum] = dataStructure[kComSum][docCombSum]

        # arranging it in ascending order by rating.
        topRes = [(k, fusedCombSUM[k]) for k in sorted(fusedCombSUM, key=fusedCombSUM.get, reverse=True)]
        return topRes

    def getEngineWeight(self, file):
        """ Returns engine and their weight """
        engineWeight = {}
        with open(file) as weights:
            for w in weights:
                wLine = w.split("\t")
                for sysw in wLine:
                    eng = sysw.split(";") #splitting it by ; to get enigine id and their weight
                    engineWeight[eng[0].strip().upper()] = float(eng[1])
        return engineWeight


if __name__ == '__main__':
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:w:o:")
      if len(opts) != 3:
          print('Please pass all the parameters: python quesOne.py -i <inputfile> -w <engineWeightFile> -o <outFile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -w <engineWeightFile> -o <outFile>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-w':
            weightFile = arg
        if opt == '-o':
            oFile = arg
    start = EvaluationModel(iFile, weightFile, oFile)
    start.evaluation()
