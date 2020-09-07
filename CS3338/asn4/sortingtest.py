numberList = [10, 9, 1000, 200, 19, 8, 7, 6, 5, 4, 3, 2, 1]

#   WANT TO IMPLEMENT SELECTION SORT

for i in range(len(numberList)):
    minIndex = i
    for j in range(i + 1, len(numberList)):
        if numberList[j] < numberList[minIndex]:
            minIndex = j
            print("The minimum element is ", numberList[minIndex])

    tempElement = numberList[i]
    numberList[i] = numberList[minIndex]
    numberList[minIndex] = tempElement

    print(numberList)

print(numberList)

