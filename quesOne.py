"""
Runs part 1 of assignment.

python3 quesOne.py
Args:
    -i inputFile.txt
    -o outputFile.txt
"""

import os
import sys, getopt
import string
from statistics import mean

# To run the script -
# python3 quesOne.py -i inputQuesOne.txt -o ouputQuesOne.txt

class Evaluation(object):
    def __init__(self, iFile, oFile):
        self.iFile = iFile
        self.oFile = oFile
        pass

    def performance(self):
        """
        This function reads the source file calculate the performance using the following techniques:
        - Precision
        - Recall
        - P@5
        - P@R=0.5
        - Average Precision
        - Mean Average precision
        - Inverted index output as a list of 11 Precision values, 1 at each of the recall thresholds.
        """
        try:
            outFile = open(self.oFile, "w")
            with open(self.iFile) as f:
                averagePrecision = {}
                for n, line in enumerate(f, 1):
                    eachLine = line.split(";")
                    relRet = eachLine[2].strip().count("R") #number of relevent documents retrieved
                    relevent = eachLine[3].strip() #number of relevent documents in the corpus
                    totalRetrieved = len(eachLine[2].strip()) #number of all the retrieved documents
                    precision = round((float(int(relRet)/int(totalRetrieved))),2) #calculating the precision value
                    recall = round((float(int(relRet)/int(relevent))),2) #calculating the recall value
                    relRetAt5 = eachLine[2].strip()[0:5].count("R") #number of relevent documents at position 5
                    pAt5 = round((float(int(relRetAt5)/int(5))),2) #calculating the precision at 5
                    splitRes = self.split(eachLine[2].strip()) #list of retrieved documents

                    precisionAtRecall = {}
                    for n, char in enumerate(splitRes, 1):
                        if char == "R":
                            relRetAtn = eachLine[2].strip()[0:n].count("R") # count of relevent document at position n
                            recallAtn = round(((int(relRetAtn)/int(relevent))*100),2) #calculates recall level
                            precisionAtn = round((float(int(relRetAtn)/int(n))),2) #precision of all the relevent documents retrieved
                            precisionAtRecall[recallAtn] = precisionAtn

                    qAvgPrecision = round((sum(precisionAtRecall.values())/int(relevent)),2) #average precision value of each query
                    interpolatedRes = self.interpolated(precisionAtRecall) #generates interpolated results

                    #dictionary of engine and their average precision for each query
                    if eachLine[1].strip().upper() in averagePrecision.keys():
                        averagePrecision[eachLine[1].strip().upper()][eachLine[0].strip()] = qAvgPrecision
                    else:
                        averagePrecision[eachLine[1].strip().upper()] = {}
                        averagePrecision[eachLine[1].strip().upper()][eachLine[0].strip()] = qAvgPrecision


                    print("\nPrecision of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), precision))
                    print("Recall of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), recall))
                    print("P@5 of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), pAt5))
                    print("P@R=0.5 of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), interpolatedRes['pAtR50']))
                    print("Average Precision of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), qAvgPrecision))
                    print("Inverted index output of 11 Precision values of run %s from engine %s is:" % (eachLine[0], eachLine[1].upper()))
                    print("Recall Level \t 100% \t 90% \t 80% \t 70% \t 60% \t 50% \t 40% \t 30% \t 20% \t 10% \t 0%")
                    print("Precision \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s" % (interpolatedRes["pAtR100"], interpolatedRes["pAtR90"],
                    interpolatedRes["pAtR80"], interpolatedRes["pAtR70"], interpolatedRes["pAtR60"], interpolatedRes["pAtR50"], interpolatedRes["pAtR40"],
                    interpolatedRes["pAtR30"], interpolatedRes["pAtR20"], interpolatedRes["pAtR10"], interpolatedRes["pAtR0"]))

                    outFile.write("\nPrecision of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), precision))
                    outFile.write("\nRecall of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), recall))
                    outFile.write("\nP@5 of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), pAt5))
                    outFile.write("\nP@R=0.5 of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), interpolatedRes['pAtR50']))
                    outFile.write("\nAverage Precision of run %s from engine %s is: %.2f" % (eachLine[0], eachLine[1].upper(), qAvgPrecision))
                    outFile.write("\nInverted index output of 11 Precision values of run %s from engine %s is:" % (eachLine[0], eachLine[1].upper()))
                    outFile.write("\nRecall Level \t 100% \t 90% \t 80% \t 70% \t 60% \t 50% \t 40% \t 30% \t 20% \t 10% \t 0%")
                    outFile.write("\nPrecision \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s\n" % (interpolatedRes["pAtR100"], interpolatedRes["pAtR90"],
                    interpolatedRes["pAtR80"], interpolatedRes["pAtR70"], interpolatedRes["pAtR60"], interpolatedRes["pAtR50"], interpolatedRes["pAtR40"],
                    interpolatedRes["pAtR30"], interpolatedRes["pAtR20"], interpolatedRes["pAtR10"], interpolatedRes["pAtR0"]))


                #calculating Mean Average Precision
                print("\n")
                dictMeanAvgPrecision = {}
                for key in averagePrecision.keys():
                    mAvgPrecision = round(mean(averagePrecision[key].values()),2)
                    dictMeanAvgPrecision[key] = mAvgPrecision
                    print("Mean Average Precision of engine %s is: %.2f" % (key, mAvgPrecision))
                    outFile.write("\nMean Average Precision of engine %s is: %.2f" % (key, mAvgPrecision))

                #calculating top three engines wihch performs best
                systemPerformance = [(k, dictMeanAvgPrecision[k]) for k in sorted(dictMeanAvgPrecision, key=dictMeanAvgPrecision.get, reverse=True)]
                print("\nTop three engines are:")
                outFile.write("\n\nTop three engines are:")
                i = 1
                for k, val in systemPerformance[0:3]:
                    print("%d. Engine %s with Mean Average Precision %.2f " % (i, k, val))
                    outFile.write("\n%d. Engine %s with Mean Average Precision %.2f " % (i, k, val))
                    i = i+1

                outFile.close()

        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

    def split(self, word):
        return [char for char in word]

    def interpolated(self, precisionAtRecall):
        """this function generates interpolated resultes"""

        interpolatedPatR = {'pAtR0': [0], 'pAtR10': [0], 'pAtR20': [0], 'pAtR30': [0],
        'pAtR40': [0], 'pAtR50': [0], 'pAtR60': [0], 'pAtR70': [0], 'pAtR80': [0], 'pAtR90': [0], 'pAtR100': [0]}
        for recall in precisionAtRecall.keys():
            if recall == 100:
                interpolatedPatR['pAtR100'].append(precisionAtRecall[recall])
            if recall >= 90 and recall <= 100:
                interpolatedPatR['pAtR90'].append(precisionAtRecall[recall])
            if recall >= 80 and recall <= 100:
                interpolatedPatR['pAtR80'].append(precisionAtRecall[recall])
            if recall >= 70 and recall <= 100:
                interpolatedPatR['pAtR70'].append(precisionAtRecall[recall])
            if recall >= 60 and recall <= 100:
                interpolatedPatR['pAtR60'].append(precisionAtRecall[recall])
            if recall >= 50 and recall <= 100:
                interpolatedPatR['pAtR50'].append(precisionAtRecall[recall])
            if recall >= 40 and recall <= 100:
                interpolatedPatR['pAtR40'].append(precisionAtRecall[recall])
            if recall >= 30 and recall <= 100:
                interpolatedPatR['pAtR30'].append(precisionAtRecall[recall])
            if recall >= 20 and recall <= 100:
                interpolatedPatR['pAtR20'].append(precisionAtRecall[recall])
            if recall >= 10 and recall <= 100:
                interpolatedPatR['pAtR10'].append(precisionAtRecall[recall])
            if recall >= 0 and recall <= 100:
                interpolatedPatR['pAtR0'].append(precisionAtRecall[recall])

        for key in interpolatedPatR:
            interpolatedPatR[key] = max(interpolatedPatR[key]) #taking the maximum value of all the precision at each level

        return interpolatedPatR


if __name__ == '__main__':
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:o:")
      if len(opts) != 2:
          print('Please pass all the parameters: python3 quesOne.py -i <inputfile> -o <outputfile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -o <outputfile>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-o':
            oFile = arg
    start = Evaluation(iFile, oFile)
    start.performance()
