"""
Runs part 3 of assignment.

python3 quesThree.py
Args:
    -i inputFile.txt
    -k number of sectors
    -l liveFile.txt
    -o outputFile.txt
"""

import os
import sys, getopt
import string, time
import ast

# To run the script -
# python3 quesThree.py -i inputQuesThree.txt -k 3 -l inputTwoQuesThree.txt -o outputQuesThree.txt

class Probfuse(object):
    def __init__(self, iFile, sector, liveFile, outFile):
        self.iFile = iFile
        self.sector = sector
        self.liveFile = liveFile
        self.outFile = outFile
        pass

    def model(self):
        """This function applies the probfuse model and prints the top 20 results"""
        try:
            outFile = open(self.outFile, "w")
            outFile.write("Top 20 documents from Probfuse results:\n")
            outFile.write("Rank \t Document \t Rating\n")
            print("Top 20 documents from Probfuse results:")
            print("Rank\tDocument Rating")
            with open(self.iFile) as f:
                dataStructure = {}
                noOfQuery = {}
                for line in f:
                    l = line.split(";")
                    sec = int(len(l[2].strip())/int(self.sector)) #calculating number of doc in one sector
                    qStart = 0
                    qend = sec
                    querySec = []
                    index = 0
                    #calculating precision for each sector on each query
                    while(qStart < len(l[2].strip())):
                        queryString = (l[2].strip()[qStart:qend]).count("R")
                        precision = round(float(queryString/sec), 2)
                        querySec.append(precision) #list of precision for each query
                        qStart = qStart + sec
                        qend = qend + sec
                        index = index + 1

                    # map of number of queries for each system
                    if l[1].strip().upper() in noOfQuery.keys():
                        noOfQuery[l[1].strip().upper()].append(l[0].strip())
                    else:
                        noOfQuery[l[1].strip().upper()] = []
                        noOfQuery[l[1].strip().upper()].append(l[0].strip())

                    # map of system and list of addition of precision for all the queries of that system
                    if l[1].strip() in dataStructure.keys():
                        dataStructure[l[1].strip().upper()] = [round(sum(x),2) for x in zip(dataStructure[l[1].strip().upper()], querySec)]
                    else:
                        dataStructure[l[1].strip().upper()] = querySec

            # dividing the precision by number of queries and after that dividing it with number of sector.
            for key in dataStructure.keys():
                dataStructure[key] = [round((x/len(noOfQuery[key]))/i, 2) for i, x in enumerate(dataStructure[key],1)]

            #processiong the live data with probfuse model
            probFuseResult = self.liveDataProcess(dataStructure, self.liveFile, sec)

            #writing and printing the top 20 result
            for rank, r in enumerate(probFuseResult[0:20],1):
                outFile.write("%d \t\t\t %d \t\t\t %.2f\n" % (rank, r[0], r[1]))
                print("%d \t %d \t %.2f" % (rank, r[0], r[1]))

            outFile.close()
        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

    def liveDataProcess(self, dataStructure, liveFile, sector):
        """ This function process the live data"""
        try:
            with open(liveFile) as f:
                docList = {}
                for sys in f:
                    sysLine = sys.split("\t") #spliting the data by tab
                    for elem in sysLine:
                        data = elem.split(";") #spliting the record by ;
                        secDup = sector
                        rateIndex = 0
                        docList[data[0].strip().upper()] = {}
                        listDocList = ast.literal_eval(data[1]) # converting the string of list to list object

                        #Creating map of each systems document and their rating from probfuse model using sector value
                        for ind, document in enumerate(listDocList,0):
                            if ind < secDup:
                                docList[data[0].strip().upper()][document] = dataStructure[data[0].strip().upper()][rateIndex]
                            else:
                                rateIndex = rateIndex + 1
                                secDup = secDup + sector
                                docList[data[0].strip().upper()][document] = dataStructure[data[0].strip().upper()][rateIndex]

            # applying fusion among all systems documents
            probRes = self.fuseDocuments(docList)
            return probRes

        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

    def fuseDocuments(self, dataStructure):
        """ This function applies the fusion among all systems documents """
        fusedProbfuse = {}
        for kComSum in dataStructure.keys():
            docListProbfuse = list(dataStructure[kComSum].keys())

            # adding the same documents rating from different systems and creating map of it.
            for docCombSum in docListProbfuse:
                if docCombSum in fusedProbfuse.keys():
                    fusedProbfuse[docCombSum] = round(float(fusedProbfuse[docCombSum] + dataStructure[kComSum][docCombSum]),2)
                else:
                    fusedProbfuse[docCombSum] = dataStructure[kComSum][docCombSum]
        # arranging it in ascending order by rating.
        topRes = [(k, fusedProbfuse[k]) for k in sorted(fusedProbfuse, key=fusedProbfuse.get, reverse=True)]
        return topRes

if __name__ == '__main__':
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:k:l:o:")
      if len(opts) != 4:
          print('Please pass all the parameters: python3 quesThree.py -i <inputfile> -o <number of sectors(range 3 to 20)> -l <livefile> -o <outputfile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -o <number of sectors(range 3 to 20)> -l <livefile> -o <outputfile>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-k':
            sector = int(arg)
        if opt == '-l':
            liveFile = arg
        if opt == '-o':
            outFile = arg
    if sector >= 3 and sector <= 20:
        start = Probfuse(iFile, sector, liveFile, outFile)
        start.model()
    else:
        print("Please pass the k value between 3 to 20")
