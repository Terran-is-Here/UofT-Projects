## Question 1
import os 
FILENAME = "crime_and_punishment2.txt"

def fixCWD(FILENAME, PATH): #fixes filename by adjusting based on a local path
    return os.getcwd() + PATH + FILENAME 

def get_number_of_words(FILENAME): 
    
    with open(FILENAME,encoding='utf-8') as book:
        book_text = book.read().split() 
        out = {}
        for word in book_text: 
            if word not in out: #if word has not already been counted: 
                out[word] = 1 # Define as one
            else: 
                out[word] += 1 # Increment by one 
    return out  

def top10(L): # requires us to sort L! 
    #will implement via bubble sort (descending order)
    #Bubble Sort -> O(n^2) time complexity
    hasSwapped = True 
    swaps = 0 
    while hasSwapped: 
        hasSwapped = False 
        for i in range(0,len(L)-1-swaps): 
            if L[i] < L[i+1]: #if current element larger than next element, bubble up
                L[i],L[i+1] = L[i+1],L[i] #swap numbers! 
                hasSwapped = True 
        swaps += 1 
    return L[0:9] #return top 10 integers in L

def sort_dict(D): 
    # first, convert dictionary to an .items equivalent whilst maintaining values with the same amt. 
    dict_value_holder = []
    for key,val in D.items() : 
        dict_value_holder.append((val,key)) #preserves all duplicate values as now the leading element 

    dict_value_holder = sorted(dict_value_holder)

    top_10_values = dict_value_holder[-10:]
    out = []
    for word in top_10_values: 
        out.append(word[1]) #access key value from tuple and append it to out 

    return out 

if __name__ == "__main__": 
    print(get_number_of_words(fixCWD(FILENAME,"\\Lab 7\\")))
    print(sort_dict(get_number_of_words(fixCWD(FILENAME,"\\Lab 7\\"))))
   # print(get_number_of_words(FILENAME))

## Question 2
