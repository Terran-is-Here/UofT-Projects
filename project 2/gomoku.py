"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 19, 2026
"""



OPEN_FLAG = "OPEN" 
SEMIOPEN_FLAG = "SEMIOPEN"
CLOSED_FLAG = "CLOSED"
WIN_LENGTH = 5
import copy


def is_empty(board):
    """Check if the board is fully empty. Returns True if it is, False if not. """
    for row in board:
        for elem in row: 
            if elem != " ": 
                return False
    return True

def is_full(board): 
    """Check if the board is full. Returns True if it is, False if not. """
    for row in board:
        for elem in row: 
            if elem == " ": 
                return False
        return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """Checks a sequence of length length that ends (y_end,x_end)'s boundedness. """
    # Get values of endpoints and start point
    afterEndY = y_end + d_y
    afterEndX = x_end + d_x
    startY = y_end - (d_y * length) #double check (off by one?)
    startX = x_end - (d_x * length) #double check (off by one?)
    board_size = len(board) - 1 #offset indexing
    open_spaces = 2 #number of valid spaces 

    # Check if these values are a "wall" (that is, outside the bounds of the table)
    if board_size < afterEndY or afterEndY < 0 or board_size < afterEndX or afterEndX < 0: 
        open_spaces -= 1
    else: 
        if board[afterEndY][afterEndX] != " ": # Check if tile is not free
            open_spaces -= 1

    # Do the same for the starting values
    if board_size < startY or startY < 0 or board_size < startX or startX < 0: 
        open_spaces -= 1
    else: 
        if board[startY][startX] != " ": # Check if tile is not free
            open_spaces -= 1

    if open_spaces == 2: # Return corresponding values pertaining to boundedness.
        return OPEN_FLAG
    elif open_spaces == 1: 
        return SEMIOPEN_FLAG
    else: 
        return CLOSED_FLAG

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    """
    Analyses the row R from (y_start,x_start) in the direction of d_y,d_x, and returns a tuple of 
    open sequences in R, and semi-open sequences in R of the color col. 
    """
    open_seq_count = 0
    semi_open_seq_count = 0 
    samecolor_count = 0 
    # Go through list, check if color is the same, count length, if length of count is same as length, check openness. 
    board_value = ""
    seq_state = ""
    # Find bound for how long we're checking 
    d_x_max  = max(d_x*(len(board)-x_start),-1*d_x*x_start)
    d_y_max = max(d_y*(len(board)-y_start),-1*d_y*y_start)

    if d_y == 0: # If Y is not being traversed, bound with terms to x
        bound = d_x_max
    elif d_x == 0: # If X is not being traversed, bound with terms of y
        bound = d_y_max 
    else: # If both are being traversed, bound with terms of the minimum value of the two above. 
        bound = min(d_x_max,d_y_max)

    for i in range(bound):  #check length of board: 
        # Get corresponding test values 
        check_x = x_start +  d_x*i  #
        check_y = y_start + d_y*i
        # Get corresponding board value 
        board_value = board[check_y][check_x]
        
        if board_value == col: #If color is the same as the one we are checking, 
            samecolor_count += 1 # Iterate count by one
        else: #If sequence is broken... 
            if samecolor_count == length: #If sequence length is EXACTLY the length; then it is complete, thus we check it. 
                seq_state = is_bounded(board,check_y-(1*d_y),check_x-(1*d_x),length,d_y,d_x) #Check from point right before the sequence breaks. 
                if seq_state == OPEN_FLAG: 
                    open_seq_count += 1
                elif seq_state == SEMIOPEN_FLAG:
                    semi_open_seq_count += 1
            else: #If sequence length is not exact, do not count. (e.g. bbbb, w/length 3, subsequence, or bb not length 3)
                pass
            samecolor_count = 0 #Reset count
            continue 
        
             

    return open_seq_count, semi_open_seq_count

# Variant of Detect_Row, instead returning the number of complete sequences
# of color col, and of length length. 
def detect_sequences_of_length(board,col,y_start,x_start,length,d_y,d_x): 
    seq_count = 0
    samecolor_count = 0 
    # Go through list, check if color is the same, count length, if length of count is same as length, check openness. 
    board_value = ""

    # Find bound for how long we're checking 
    d_x_max  = max(d_x*(len(board)-x_start),-1*d_x*x_start)
    d_y_max = max(d_y*(len(board)-y_start),-1*d_y*y_start)

    if d_y == 0: 
        bound = d_x_max
    elif d_x == 0: 
        bound = d_y_max 
    else: 
        bound = min(d_x_max,d_y_max)

    for i in range(bound):  #check length of board: 
            # Get corresponding test values 
            check_x = x_start +  d_x*i  #get test x value
            check_y = y_start + d_y*i #get test y value
            # Get corresponding board value 
            board_value = board[check_y][check_x]
            
            if board_value == col: #If color is the same as the one we are checking, 
                samecolor_count += 1 # Iterate count by one
            
            else: #If sequence is broken...  
                if samecolor_count == length: #If sequence length is EXACTLY the length; then it is complete. 
                    seq_count += 1 
                else: #If sequence length is not exact (e.g. bbbb, w/length 3, subsequence)
                    pass
                samecolor_count = 0 #Reset count
                continue 
            

    return seq_count #return count of complete sequences with length length...

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    # Check Vertical Rows, use top row for analysis 
    for column in range(len(board)): 
        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,0,column,length,1,0) 
        
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

    #Check Horizontal Rows
    for row in range(len(board)): 
        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,row,0,length,0,1) 
        
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

    # Check Diagonals from the top
    for column in range(len(board)): 
        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,0,column,length,1,1) # towards bottom right 
        
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,0,column,length,1,-1) # towards bottom left 
                    
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

    # Check Diagonals from the bottom
    for column in range(1,len(board)-1): 
        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,len(board)-1,column,length,-1,1) # towards top right 
        
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

        open_seq_buffer,semiopen_seq_buffer = detect_row(board,col,len(board)-1,column,length,-1,-1) # towards top left 
                    
        open_seq_count += open_seq_buffer
        semi_open_seq_count += semiopen_seq_buffer

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    top_score = 0
    temp_score = 0
    board_copy = []
    for temp_move_y in range(len(board)):  #Iterate through all possible y placements, 
        for temp_move_x in range(len(board)): # Iterate through all possible x placements
            if board[temp_move_y][temp_move_x] == " ": #check if we can place
                board_copy = copy.deepcopy(board) #if we can place, make a copy of the board
                board_copy[temp_move_y][temp_move_x] = "b" #set test token 
                temp_score = score(board_copy) #then score the test board

                if temp_score == 100000: #If winning move is detected
                    return temp_move_y, temp_move_x #return winning move immediately. 
                
                if temp_score > top_score: #if temporary score is greater than the top score, we set that as the next best move. 
                    top_score = temp_score
                    move_y = temp_move_y
                    move_x = temp_move_x
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
    
def is_win(board):
    
    win_states = ["White won", "Black won", "Draw", "Continue playing"]
    colors = ["w","b"]
    # Check per color
    
    for col in colors: 
        winning_rows = 0
        for column in range(len(board)): 
            winning_rows += detect_sequences_of_length(board,col,0,column,WIN_LENGTH,1,0) 

        #Check Horizontal Rows
        for row in range(len(board)): 
            winning_rows += detect_sequences_of_length(board,col,row,0,WIN_LENGTH,0,1) 

        # Check Diagonals from the top
        for column in range(len(board)): 
            winning_rows += detect_sequences_of_length(board,col,0,column,WIN_LENGTH,1,1) # towards bottom right 
            winning_rows += detect_sequences_of_length(board,col,0,column,WIN_LENGTH,1,-1) # towards bottom left 

        # Check Diagonals from the bottom
        for column in range(1,len(board)-1): 
            winning_rows += detect_sequences_of_length(board,col,len(board)-1,column,WIN_LENGTH,-1,1) # towards top right 
            winning_rows+= detect_sequences_of_length(board,col,len(board)-1,column,WIN_LENGTH,-1,-1) # towards top left 

        if winning_rows != 0: #if a winning row exists, return the corresponding color. 
            return win_states[colors.index(col)]
    # If no color wins, check if board is full: 
    return win_states[2] if is_full(board) else win_states[3]


            

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(f"Detect Row Result: {detect_row(board,"w",0,x,length,d_y,d_x)}, Desired: (1,0)")
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

if __name__ == '__main__':
    easy_testset_for_main_functions()
    play_gomoku(8)
    
