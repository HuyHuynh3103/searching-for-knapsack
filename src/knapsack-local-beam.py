import time
import utils.read
import utils.write

def LocalBeam(capacity, num, Wlist, VList, Clabel, Bwidth):
    highest_val = float
    path = [(tuple(), 0, 0, tuple())]

    for i in range(len(VList)):
        pathtier = []

        for j in range(len(path)):
            item, val, weight, classes = path[j]
            # Filter out paths that violate the weight constraint during path generation
            for k in range(len(VList)):
                if(k not in item and weight + Wlist[k] <= capacity):
                    newitem = set(item).copy()
                    newitem.add(k)
                    newitem = tuple(newitem)
                    updateclass = set(classes).copy()
                    updateclass.add(Clabel[k])
                    updateclass = tuple(updateclass)
                    nextpath = (newitem,val+VList[k], weight+Wlist[k],updateclass)

                else:
                    nextpath = (item,val,weight,classes)
                pathtier.append(nextpath)
        # Add randomness to path selection for diversity
        path_order = sorted(pathtier,key = lambda element:(len(element[3]), element[1],capacity-element[2]), reverse = True)
        path_order = list(sorted(set(path_order), key = path_order.index))
        path = path_order[:Bwidth]

    best_track = [0]*len(VList)
    best_path = path[0]

    temp = []
    for x in best_path[0]:
        best_track[x] = 1
        if(best_track[x] == 1):
            temp.append(Clabel[x]) 
            
    # Ensure that the selected items cover all classes
    for y in range(1,num):
        if (sorted(temp)).count(y) == 0:
            return 0,0


    highest_val = best_path[1]
    return  highest_val,best_track



if __name__ == '__main__':
    print("==Local Beam Solution==")
    w, m, WList, VList, Clabel = utils.read.readDataset()
    start = time.time()
    for x in range(1,9):
        lb = LocalBeam(w,m,WList,VList,Clabel,x)
        for y in range(2,len(WList)):
            best_val = LocalBeam(w,m,WList,VList,Clabel,x)
    end = time.time()
    utils.write.writeOutput(best_val[0], best_val[1])
    print("Time: ", end - start, '\n')
    
