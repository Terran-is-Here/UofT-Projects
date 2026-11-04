import numpy as np
import copy

def print_matrix(M_lol): 
    print(np.array(M_lol))


def get_lead_ind(row): 
    for i in range(len(row)): 
        if row[i] != 0: # Find index of first non-zero element and return it 
            return i

    return len(row) # If not, return the length of row. 

def get_row_to_swap(M, start_i): 
    # return index of row that needs to be swapped with M[start_i]. 
    # Row that needs to be swapped with M[start_i] is the row at row at the index >= start_i where the leading coefficient is left-maximized. 

    current_min_coefficient = 10000000000000 #some absurdly high number 
    index_to_return = 0
    for i in range(start_i, len(M)):  #Go from index -> length of list
        current_row = M[i] #get current row 
        buffer = get_lead_ind(current_row) #check leading index of leading 1 
        if current_min_coefficient >= buffer: # if index of leading 1 is less than previous record, it is more towards the left then
            current_min_coefficient = buffer # update record
            index_to_return = i # increment index

    return index_to_return

def add_row_coefs(r1,c1,r2,c2): 
    output = [0]*len(r1)
    for i in range(len(r1)): #since len(r1)=len(r2)
        buffer = r1[i]*c1 + r2[i]*c2 
        output[i]=buffer
    return output 

def eliminate(M, row_to_sub, best_lead_ind): 
    leading_coef_in_rts = row_to_sub[best_lead_ind]
    for i in range(M.index(row_to_sub)+1, len(M)): # go from row_to_sub+1 to M downwards. 
        leading_coeff = M[i][best_lead_ind] 
        c =  (-1*leading_coeff)/leading_coef_in_rts
        # c1 + rc2 = 0 -> -c1/c2
        print(f"c term: {c}")
        M[i] = add_row_coefs(row_to_sub,c,M[i],1)

def upwards_elimination(M,row_to_sub,best_lead_ind): 
    leading_coef_in_rts = row_to_sub[best_lead_ind]
    for i in range(M.index(row_to_sub)-1, -1, -1): # go from row_to_sub+1 to 0 upwards. 
        leading_coeff = M[i][best_lead_ind] 
        c =  (-1*leading_coeff)/leading_coef_in_rts
        # c1 + rc2 = 0 -> -c1/c2
        print(f"c term: {c}")
        M[i] = add_row_coefs(row_to_sub,c,M[i],1)

def forward_step(M): 

    # First, sort rows
    for i in range(len(M)): 
        row_swap_index = get_row_to_swap(M,i) # Get corresponding swap index
        print("="*10)
        print_matrix(M)
        print(f"Swapping row{i} with row{row_swap_index}" if i!= row_swap_index else "No row swap in this step.")
        
        temp = copy.copy(M[i]) #temporary make a copy (grr aliasing) 
        M[i] = copy.copy(M[row_swap_index]) # Swap row / mem assignments 
        M[row_swap_index] = temp #then reassign temp to swapped row in turn. 
        print_matrix(M)

    
    # Since rows are now sorted...
    for i in range(len(M)): 
        row_to_sub = M[i]
        best_lead_ind = get_lead_ind(row_to_sub)
        print("="*10)
        print_matrix(M)
        print(f"Eliminating row{i}'s leading term from the rest of the matrix")
        eliminate(M,row_to_sub,best_lead_ind)
        print_matrix(M)

def backward_step(M): 

    # Perform an Upwards Elimination
    for i in range(len(M)): 
        row_to_sub = M[i]
        best_lead_ind = get_lead_ind(row_to_sub)
        print("="*10)
        print_matrix(M)
        print(f"Eliminating row{i}'s leading term from the rest of the matrix")
        upwards_elimination(M,row_to_sub,best_lead_ind)
        print_matrix(M)

    # Then set rows to 1
    for i in range(len(M)): 
        row_to_manipulate = M[i] 
        leading_value = row_to_manipulate[get_lead_ind(row_to_manipulate)]
        M[i] = add_row_coefs(row_to_manipulate, 1/leading_value,M[i],0) #second matrix does NOT matter at all.


def solve(A,b): 
    # first, generate augmented matrix 
    M = []
    for i in range(len(A)): #A and B share the same amount of rows
        temp = []
        temp.extend(A[i])
        temp.append(b[i])
        
        M.append(temp) 
    for i in range(len(M)): 
        row_swap_index = get_row_to_swap(M,i) # Get corresponding swap index
        print("="*10)
        print_matrix(M)
        print(f"Swapping row{i} with row{row_swap_index}" if i!= row_swap_index else "No row swap in this step.")
        
        temp = copy.copy(M[i]) #temporary make a copy (grr aliasing) 
        M[i] = copy.copy(M[row_swap_index]) # Swap row / mem assignments 
        M[row_swap_index] = temp #then reassign temp to swapped row in turn. 
        print_matrix(M)

    
    # Since rows are now sorted...
    for i in range(len(M)): 
        row_to_sub = M[i]
        best_lead_ind = min(get_lead_ind(row_to_sub),len(A))
        print("="*10)
        print_matrix(M)
        print(f"Eliminating row{i}'s leading term from the rest of the matrix")
        eliminate(M,row_to_sub,best_lead_ind)
        print_matrix(M)

    # Perform an Upwards Elimination
    for i in range(len(M)): 
        row_to_sub = M[i]
        best_lead_ind = min(get_lead_ind(row_to_sub),len(A))
        print("="*10)
        print_matrix(M)
        print(f"Eliminating row{i}'s leading term from the rest of the matrix")
        upwards_elimination(M,row_to_sub,best_lead_ind)
        print_matrix(M)

    # Then set rows to 1
    for i in range(len(M)): 
        row_to_manipulate = M[i] 
        leading_value = row_to_manipulate[get_lead_ind(row_to_manipulate)]
        M[i] = add_row_coefs(row_to_manipulate, 1/leading_value,M[i],0) #second matrix does NOT matter at all.

    # then obtain x, as x = b at this point; then it's equivalent to the last rows in the column. 
    out = []
    for i in range(len(M)): 
        print(i)
        out.append(M[i][len(M[i])-1])
    return out 
    

if __name__ == "__main__": 
    M = np.array([[1, -2, 3], [3, 10, 1], [1, 5, 3]])
    x = np.array([75, 10, -11])
    b = np.matmul(M, x)
    x_found = solve(M.tolist(), b.tolist())
    print(x_found) # should recover [75, 10, -11
