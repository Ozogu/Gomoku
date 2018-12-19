from tkinter import *
from tkinter.messagebox import showerror

class BoardSize():
    def __init__(self):
        self.success = False
        # Init window
        self.__window = Tk()

        # Init buttons
        self.__window.title("Board settings")
        self.__label = Label(self.__window,
                                    text = "Size of board?")
        self.__size = Entry(self.__window)
        self.__ok_button = Button(self.__window,
                                 text="Ok", command= self.take_size)

        # Default size
        self.__size.insert(0,"20")

        # Places
        self.__label.grid(row=0,column=0)
        self.__size.grid(row=1,column=0)
        self.__ok_button.grid(row=2,column=0)

        # Hotkeys
        self.__size.bind("<Return>",self.take_size)

        self.__window.mainloop()

    def take_size(self,event=""):
        """
        Take and return board size from entry
        :param event: For hotkey
        """
        try:
            # size that is returned
            self.size = int(self.__size.get())

            if self.size in range(10,36):
                self.__window.destroy()
                self.success = True
            else:
                raise Exception("Size out of bounds")
        except:
             showerror("Error!","Size must be integer between 10-35")

class Gomoku():
    def __init__(self,size):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Gomoku")

        # variables
        self.__board_size = size
        self.__turn_counter = 0
        self.__player = 1

        # Creating labels
        self.__status = Label(self.__mainwindow,text="Player {}"
                                    .format(self.__player))
        self.__turn_counter_label = Label(self.__mainwindow,text=
                            "{}. Turns taken".format(self.__turn_counter))

        # Placing label
        self.__status.grid(row=0,column=0,columnspan=4)
        self.__turn_counter_label.grid(row=0,column=4,columnspan=4)

        # Creating board
        self.__board = []
        for size_x in range(self.__board_size):
            self.__board_x = []
            for size_y in range(self.__board_size):
                # Creating button
                button = Button(self.__mainwindow,width=2,height=1,
                                      command =(lambda y=size_y,x=size_x:
                                                self.take_turn(x,y)))
                # Place button to board
                button.grid(row=size_y+1,column=size_x,sticky =N+W+E+S)
                # Place button to to list
                self.__board_x.append(button)
            self.__board.append(self.__board_x)

        self.__mainwindow.mainloop()

    def take_turn(self,x,y):
        """
        Places x or o, locks the button and passes the information
        :param x: X coordinate
        :param y: y coordinate
        :return: None
        """
        # Take player 1 turn
        if self.__player == 1:
            self.__board[x][y].config(state = DISABLED,
                                          background="lightblue",text="X")
            # Return if win condition met
            if self.check_win_condition("lightblue",[x,y]): return
        # Take player 2 turn
        elif self.__player == 2:
            self.__board[x][y].config(state = DISABLED,
                                          background="lightcoral",text="O")
            if self.check_win_condition("lightcoral",[x,y]): return
        # Update board
        self.__board[x][y].update()
        self.end_turn()

    def end_turn(self):
        """
        Update playing player and turn label
        """
        self.__turn_counter += 1
        # Update player
        self.__player %=2
        self.__player += 1
        self.__status["text"] = "Player {}".format\
            (self.__player)
        self.__turn_counter_label["text"]= "{}. Turns taken".format\
            (self.__turn_counter)
        self.__turn_counter_label.update()

    def check_win_condition(self,token,coordinate):
        """
        Check if win condition met.
        Check horizontal, vertical, and diagonal vectors for win conditions
        :param token: Player token
        :param coordinate: Coordinate of the button
        :return: True if win condition met
        """
        # Check if it's even possible to win yet
        if self.__turn_counter >= 8:
            # Up and up right vectors
            vec1=(1,0)
            vec2=(1,1)

            # Loop both directions of vector
            for _ in range(2):
                if True == self.check_direction(token,vec1,coordinate):
                    self.declare_winner()
                    return True
                if True == self.check_direction(token,vec2,coordinate):
                    self.declare_winner()
                    return True

                # Turn vector directions
                vec1 = -vec1[1], vec1[0]
                vec2 = -vec2[1], vec2[0]

        # Check for draw
        if self.__turn_counter+1 == self.__board_size**2:
            self.__turn_counter_label["text"] = "Draw!"
            self.__status["text"] = ""
            self.__status.update()
            self.__turn_counter_label.update()
            showerror("Tasapeli","tasapeli!")
            return True

    def check_direction(self, token, vector, coordinate):
        """
        Takes a vector, creates inverse vector and gives both to direction function.
        :param token: Player token
        :param vector: direction vector which will be passed forward
        :param coordinate: Coordinate of the button
        :return: True if 5-straight found.
        """
        inverse_vector = -vector[0], -vector[1]
        # Calculate hits to direction
        hits = self.direction(token,vector,1,coordinate)
        if hits == 5:
            return True
        # After reaching the end, add hits towards the opposite direction
        hits = self.direction(token,inverse_vector,hits,coordinate)
        if hits == 5:
            return True

    def direction(self, token, vector, hits, coordinate):
        """
        Calculate hits towards this direction
        :param token: Player token
        :param vector: direction vector
        :param hits:  Hits so far
        :param coordinate: Coordinate of the button
        :return:
        """
        try:
            # Button at the end to the vector
            next_x = coordinate[0]+vector[0]
            next_y = coordinate[1]+vector[1]
            next_coordinate = [next_x,next_y]
            # tarkistetaan token ja tallennetaan se uutena merkkinä
            if self.__board[next_x][next_y]["background"] == "lightcoral":
                next_token = "lightcoral"
            elif self.__board[next_x][next_y]["background"] == "lightblue":
                next_token = "lightblue"
            else:
                next_token = None

            # Add hit and continue if next token is of the players
            if next_token == token:
                hits = self.direction(next_token, vector, hits+1 ,next_coordinate)
            # Else return hits
            return hits
        # Out of bounds
        except IndexError:
            return hits

    def declare_winner(self):
        """
        Pop up winner
        """
        # Update label
        self.__turn_counter_label["text"] = "Player {} won!".format\
            (self.__player)
        self.__status["text"] = ""
        self.__status.update()

        # Disable buttons
        for x_buttons in range(len(self.__board)):
            for y_buttons in range(len(self.__board)):
                self.__board[x_buttons][y_buttons].config(state=DISABLED)
        self.__turn_counter_label.update()

        # Declare winner
        showerror("Winner","Player {} won!".format
        (self.__player))

def main():
    board_size = BoardSize()
    # Check if valid board size was gotten.
    if board_size.success == True:
        Gomoku(board_size.size)

main()
