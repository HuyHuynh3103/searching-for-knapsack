import os
def writeOutput(maxValue, listW, fileName = "../../OUTPUT_10.txt"):
    path = os.path.dirname(__file__)
    pathFileName = (path + "/" + fileName)
    with open(pathFileName, "w") as fout:
        if maxValue > 0:
            fout.write(f"{maxValue}\n")
            fout.write(f"{listW}")
        else:
            fout.write("No optimal solution")
    fout.close()