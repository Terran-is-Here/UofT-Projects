def IncrementScores():
    global scores, average
    sum = 0
    for i in range(0, len(scores)):
        score=  scores[i]
        sum += score
    average = sum/i

scores = [0,1,2]
IncrementScores()
print(average)
print(scores)

