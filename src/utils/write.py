import os
def writeOutput(highestTotalValues, solutionItems, fileName = "../../OUTPUT_10.txt"):
    path = os.path.dirname(__file__)
    pathFileName = (path + "/" + fileName)
    with open(pathFileName, "w") as fout:
        if highestTotalValues > 0:
            fout.write(f"{highestTotalValues}\n")
            fout.write(f"{solutionItems}")
        else:
            fout.write("No optimal solution")
    fout.close()