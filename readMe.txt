# Evaluation

1. I am using python3 for this assignment and the version is Python 3.7.4.
2. Any OS can be used, I have used MAC.
3. Please make sure you keep all the files in one folder and pass the correct file path where ever needed.

# Please check the following commands, arguments and description to run the programmes-

## **Question One**

Question: You must explain your ranking and evaluation system in a readme document.
Answer: I want as many of the returned documents to be relevant for that I need the precision value to be high.
instead of recall value. So I am selecting the engine which has the high Mean Average Precision value.

```
python3 quesOne.py -i <inputFile> -o <outputFile>
Args:
    -i inputFileOne.txt
    -o outputFileOne.txt

example:
python3 quesOne.py -i inputFileOne.txt -o outputFileOne.txt

```
description -:
- Precision and Recall value are not printed in percentage in question one.
- Along with the printing, results are also stored in the given output file.


## **Question Two**

```
python3 quesTwo.py -i <inputfile> -w <engineWeightFile> -o <outFile>
Args:
    -i inputFile.txt
    -w engineWeightsFile.txt
    -o ouputFile.txt

example:
python3 quesTwo.py -i inputQuesTwo.txt -w inputTwoQuesTwo.txt -o outputFileTwo.txt

```
description -:
- To get the top 100 result please pass the at least 100 documents in input file.
- Along with the printing, results are also stored in the given output file.


## **Question Three**

```
python3 quesThree.py -i <inputfile> -o <number of sectors> -l <livefile> -o <outputfile>
Args:
    -i inputFile.txt
    -k number of sectors
    -l liveFile.txt
    -o outputFile.txt

example:
python3 quesThree.py -i inputQuesThree.txt -k 3 -l inputTwoQuesThree.txt -o outputQuesThree.txt

```
description -:
- k value should be an integer and in range of 3 to 20 as per the description in the requirement.
- Format of live data is A;[26,29,57,...]
- Please do not repeat the same engine in the live data.
- Along with the printing, top 20 results are also stored in the given output file.
