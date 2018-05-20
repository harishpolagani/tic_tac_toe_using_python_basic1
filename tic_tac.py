import numpy as np
import sys

class Tick_Tac_Toe_class():
    game_state_info = ["GAME_NOT_STARTED","GAME_STARTED","GAME_RESUMED","GAME_COMPLETED"]
    def __init__(self,game_square_matrix_shape=3):
        self.game_state = 0 #state_machine of Game current state:  0 - game not started  1 - game started  2 - game resumed  3 - game completed
        self.user_input_position = 0 #actual position chosen by Player
        self.no_of_player = 2 # Restricted to 2
        self.user_input_taken_Flag = False #to ensure player has given proper input
        self.exit_flag = False #flag to exit from game
        self.count = 0 #player info Even number - PLAYER:A   Odd  number - PLAYER:B
        self.game_square_matrix_shape = game_square_matrix_shape #restricted to 3 now
        self.matrix_tic=np.zeros((game_square_matrix_shape,game_square_matrix_shape),dtype=np.int32)
    
    
    def get_matrix_dim(self):
        return self.matrix_tic.shape

    def get_current_player_name(self):
        #restricting no of players 2 for now
        if self.count % 2 == 0: return "PLAYER1"
        else: return "PLAYER2"

    def get_current_player_id(self):
        #restricting no of players 2 for now
        if self.count % 2 == 0: return 1 #"PLAYER1"
        else: return 2 #"PLAYER2"
    
    def get_matrix_printable_format_string(self):
        matrix_data="\n"
        row_size1 = 0
        column_size1 =0
        x_row,y_column = self.get_matrix_dim()
        while row_size1 < x_row :
            while column_size1 < y_column:
                matrix_data += "{0:3}".format(self.matrix_tic[row_size1,column_size1])
                column_size1 += 1
            row_size1 += 1
            column_size1 = 0
            matrix_data += "\n"
        return matrix_data
    
    def set_game_state(self,state):
        #state_machine of Game current state  
        # 0 - game not started  
        # 1 - game started  
        # 2 - game resumed  
        # 3 - game completed
        self.game_state = state
        return True

    def get_game_state(self):
        #state_machine of Game current state  
        # 0 - game not started  
        # 1 - game started  
        # 2 - game resumed  
        # 3 - game completed
        state = self.game_state
        return Tick_Tac_Toe_class().game_state_info[state]


    def validate_user_input(self,user_matrix_rows,user_matrix_columns):
        if user_matrix_rows == 'EXIT' or user_matrix_columns == 'EXIT':
            self.exit_flag = True
            sys.exit()
            return False
        else:
            if user_matrix_rows.isdigit() and user_matrix_columns.isdigit():
                user_matrix_rows = int(user_matrix_rows)
                user_matrix_columns = int(user_matrix_columns)

            max_matrix_rows,max_matrix_columns =self.get_matrix_dim()
            if type(user_matrix_rows) == int and type(user_matrix_columns) == int:
                if user_matrix_rows < max_matrix_rows and user_matrix_columns < max_matrix_columns:
                    return True
                else:
                    print("please enter row/column with in range of matrix")
                    return False
            else:
                print("please enter only valid digits for row/column")
                return False

    
    def get_position_from_user(self):
        #validating user_input of dimension
        valid_user_input = False
        while not valid_user_input:
            user_matrix_rows = input("enter the row value / enter EXIT to exit  : ")
            if user_matrix_rows != "EXIT":
                #if user wants to exit while reading row value then there is no point in asking column value
                user_matrix_columns = input("enter the column value / enter EXIT to exit : ")
            else:
                # to avoid UnboundLocalError: local variable 'user_matrix_columns' referenced before assignment 
                user_matrix_columns = "EXIT"

            if self.validate_user_input(user_matrix_rows,user_matrix_columns):
                valid_user_input = True
        
        return int(user_matrix_rows),int(user_matrix_columns)

    def set_position_chosen_by_user(self,user_matrix_rows,user_matrix_columns,player):
        self.matrix_tic[user_matrix_rows,user_matrix_columns]=player
        self.count += 1 #increase count for next player turn
        return True

    def check_win_condition(self,player_id):
        # Matrix 'A' is:
        #  1 2 3
        #  4 5 6
        #  7 8 9
        # Matrix of A[0]  : row0                                    ==> array([1, 2, 3])
        # Matrix of A[1]  : row1                                    ==> array([4, 5, 6])
        # Matrix of A[2]  : row2                                    ==> array([7, 8, 9])
        # Diagonal matrix of A is: numpy.diag(A)                    ==> array([1, 5, 9])
        # cross diagonal Matrix of A: numpy.diag(numpy.fliplr(A))   ==> array([3, 5, 7])
        # matrix B = numpy.transpose(A)
        # 1 4 7
        # 2 5 8
        # 3 6 9
        # Matrix of B[0]  : Column0                                 ==> array([1, 4, 7])
        # Matrix of B[1]  : Column1                                 ==> array([2, 5, 8])
        # Matrix of B[2]  : Column2                                 ==> array([3, 6, 9])
        # 
        # required matrix of player1 = [1, 1, 1]
        # required matrix of player1 = [2, 2, 2]
        # winning condition check if A[0] or A[1] or A[2] or B[0]or B[1] or B[2] or Diag and cross-diag are == player1 or player2
        # ====================================================================================
        #
        #here base matrice restricted to 3X3 matrice
        player1_check_matrice = np.full((1,self.game_square_matrix_shape),1,dtype=np.int32)
        player2_check_matrice = np.full((1,self.game_square_matrix_shape),2,dtype=np.int32)

        row,column=self.matrix_tic.shape
        row_base = 0
        column_base =0
        
        Temp_matrice = self.matrix_tic
        Temp_transpose_matrice = np.transpose(Temp_matrice)
        diag_matrice = np.diag(Temp_matrice)
        cross_diag_matrice = np.diag(np.fliplr(Temp_matrice))

        if player_id == 1:
            if np.array_equal( diag_matrice , player1_check_matrice[0]):
                return True
            if np.array_equal( cross_diag_matrice , player1_check_matrice[0]):
                return True
        
        if player_id == 2:
            if np.array_equal( diag_matrice , player2_check_matrice[0]):
                return True
            
            if np.array_equal( cross_diag_matrice , player2_check_matrice[0]):
                return True
        
        # compare A[n] rows
        while row_base < row:
            if player_id == 1:
                if np.array_equal( Temp_matrice[row_base] , player1_check_matrice[0]):
                    return True
            
            if player_id == 2:
                if np.array_equal( Temp_matrice[row_base] , player2_check_matrice[0]):
                    return True
            row_base += 1

        # compare A[n] columns using transpose matrice
        while column_base < column:
            if player_id == 1:
                if np.array_equal( Temp_transpose_matrice[column_base] , player1_check_matrice[0]):
                    return True
            if player_id == 2:
                if np.array_equal( Temp_transpose_matrice[column_base] , player2_check_matrice[0]):
                    return True
            column_base += 1
        return False
    
    # playing Tic_Tac_Toe game
    def play_game(self):
        
        print("Game status= ",self.get_game_state())
        print("No. of players = ",self.no_of_player)

        #set game status to 1 i.e.. "game started"
        self.set_game_state(1)

        while not self.exit_flag:
            player_name=self.get_current_player_name()
            player=self.get_current_player_id()
            print(self.get_matrix_printable_format_string())
            print("Its",player_name,"Turn")
            row,column = self.get_position_from_user()
            self.set_position_chosen_by_user(row,column,player)
            if self.count >= self.game_square_matrix_shape-1:
                if self.check_win_condition(player):
                    print("**************************")
                    print("__________HURRAY__________")
                    print("Game over:")
                    print("winner is:  ",player_name)
                    print("**************************")
                    self.exit_flag = True


    def __str__(self):
        return "  {0} ".format(self.get_matrix_printable_format_string())



   
if __name__ == "__main__":
    Tick_Tac_Toe_class().play_game()
