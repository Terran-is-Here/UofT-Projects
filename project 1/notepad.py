my_list = [1,2,3,4]

def slice_loop(l,start,end,step): 
    out = []
    for i in range(start,end,step): 
        out.append(l[i])
    return out 


print(slice_loop(my_list,))