import numpy as np
from matplotlib import pyplot as plt
data = [('science', 42.30769230769231), ('worldnews', 36.81318681318682), ('politics', 31.318681318681318), ('economics', 27.472527472527474), ('technology', 26.923076923076923), ('programming', 22.52747252747253), ('philosophy', 17.582417582417584), ('drugs', 14.285714285714285), ('history', 10.43956043956044), ('fitness', 9.340659340659341), ('law', 7.6923076923076925), ('lgbt', 7.6923076923076925), ('religion', 6.043956043956044), ('truegaming', 3.8461538461538463), ('cooking', 3.296703296703297)]
def test():
    plt.plot([1,2,3],[3,4,3])
    ax = plt.gca()
    ax.set_xticks([1,2,3])
    ax.set_xticklabels(['cooking','somthing','fuck'])
    plt.show()
    return
def graph(dataSet):
    sortedData = sorted(dataSet,key=lambda word:word[1],reverse=True)
    lenT = len(sortedData)
    xArray = []    
    yArray = []
    for x in range(0,lenT):
        xArray.append(sortedData[x][0])
        yArray.append(sortedData[x][1])
    w = 1
    ind = np.arange(1,lenT+1)
    plt.bar(ind-w/2,yArray,w)
    plt.title("Likelihood of /r/science post being classified into each subreddit")
    plt.xlabel("List of Subreddits")
    plt.ylabel("Assigned Scores")
    ax = plt.gca()
    ax.set_xticks(ind)
    ax.set_xticklabels(['science','worldnews','politics','economics','technology','programmin','philosophy','drugs','history','fitness','law','lgbt','religion','truegaming','cooking'])
    print(xArray)
    #plt.show()    
    
    return
def sort(dataSet):
    resultArray = []    
    for item in dataSet:
        temp = item[0]
        tempData = sorted(item[1],key=lambda word:word[1],reverse=True)
        resultData = (temp, tempData)
        resultArray.append(resultData)
    #possibleTotal = len(dataSet)
    total=0
    for item1 in resultArray:
        temp1 = item1[0].lower()
        temp2 = item1[1][0][0]
        if temp1 == temp2:
            total = total +1
    print(total)    
    return resultArray
    #test()   
graph(data)
#print(sort(data))