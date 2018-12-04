import pygame
import random
import string
import shelve


class Game(object):

    """Main game class"""
    ####################
    ## Class Variables
    ####################
    
    colors = ['red', 'blue', 'green', 'yellow', 'pink', 'orange']
    colors_attribute = {'red':(255,0,0), 'blue':(0,0,255), 'green': (0,255,0), 'yellow': (255,255,0), 'pink': (255,0,255), 'orange': (255,165,0)}
    random_list = [0,1,2,3,4,5]
    run = True
    xs = [200, 600]
    dict_buttons = {}
    
    ###################
    ###################

    
    def __init__(self, win):

        self.colorname = random.choice(self.colors)   #random color selection
        self.color_att = self.colors_attribute[self.colorname]  #assigning color_attributes
        self.x = random.choice(self.xs)
        self.y = -20   #new circle starts at y=-20
        self.win = win 
        self.__score = 0 #starts with score 0
        
        self.create_buttons()  #create the buttons and run the main game loop
        self.game_mainloop()

    def create_buttons(self):

        font = pygame.font.Font("freesansbold.ttf", 25)
        pygame.draw.rect(self.win, (0,0,0), (250, 250, 300, 450))
        self.print_buttons(self.colors[self.random_list[0]], 275, 325)
        self.print_buttons(self.colors[self.random_list[1]], 425, 325)
        self.print_buttons(self.colors[self.random_list[2]], 275, 475)
        self.print_buttons(self.colors[self.random_list[3]], 425, 475)
        self.print_buttons(self.colors[self.random_list[4]], 275, 625)
        self.print_buttons(self.colors[self.random_list[5]], 425, 625)
        

        
    def print_buttons(self, color_name, x, y):

        font = pygame.font.Font("freesansbold.ttf", 25)
        label = font.render(color_name.upper(), 1, self.colors_attribute[color_name])
        self.win.blit(label, (x, y))
        self.dict_buttons[color_name] = (x - 25, y - 75)
        
    ######################################################################
    #### GETTERS AND SETTERS
    ######################################################################    
        
    def get_color_att(self):

        return self.color_att

    def get_x(self):

        return self.x

    def get_y(self):

        return self.y
    
    def get_win(self):

        return self.win
    
    def set_x(self, x):

        self.x = x

    def set_y(self, y):

        self.y = y

    def set_score(self, score):

        self.__score = score

    def set_colorname(self, color_name):

        self.colorname = color_name
        
    def get_score(self):

        return self.__score

    ##########################################################################
    #########################################################################
    
    def change_y(self):         #increases y-coordinate by 7

        self.set_y(self.y + 7)

    def draw(self):   #draws the ball and call function create buttons
        
        self.win.fill((255,255,255))
        self.print_score()
        pygame.draw.circle(self.win, self.get_color_att(), (self.x, self.y), 50)
        self.create_buttons()

    def game_mainloop(self):
        ####################### MAIN LOOP OF GAME  ##########################
        while self.run:
            
              
              self.draw()
              self.make_window()

              for event in pygame.event.get():

                  if event.type == pygame.QUIT or self.y > 750:

                      self.run = False
                   
                  if event.type == pygame.MOUSEBUTTONDOWN:
                      mx, my = pygame.mouse.get_pos()
                      if mx > 250 and mx < 550 and my > 250 and my < 700:

                           self.run = self.button_clicked(mx, my, self.colorname, self.dict_buttons)


                           
              self.change_y()
              
    #####################################################
    ## check if correct button was clicked
    #####################################################
              
    def button_clicked(self, mx, my, colorname, dict_buttons):

        real_x_pos = dict_buttons[colorname][0]
        real_y_pos = dict_buttons[colorname][1]
        
        if mx > real_x_pos and mx < real_x_pos + 150 and my > real_y_pos and my < real_y_pos + 150:

                self.new_circle_fall()
                self.set_score(self.get_score() + 1)
                return True 
              
        return False

    ######################################################
    ## Making window and executing delay
    ######################################################
    
    def make_window(self):
        
        pygame.display.flip()
        delay_time  = 10 - self.get_score()
        if delay_time < 0:
            delay_time = 0
        pygame.time.delay(delay_time)
        
    ########################################################
    ## Assiging variable so that a new ball would fall
    ########################################################
        
    def new_circle_fall(self):

        self.set_colorname(random.choice(self.colors))
        self.color_att = self.colors_attribute[self.colorname]
        self.set_x(random.choice(self.xs))
        self.set_y(-10)
        random.shuffle(self.random_list)
        self.dict_buttons.clear()
    
    #########################################################
    ## Score printing function
    #########################################################
        
    def print_score(self):

        total = "SCORE: " + str(self.get_score())
        font = pygame.font.Font("freesansbold.ttf", 25)
        label = font.render(total, 1, (0,0,0))
        self.win.blit(label, (650, 20))
 
        
#############################################################
### Maintaing everything, including calling the game mainloop
#############################################################
        
def main():
    
    restart_game = True    ##boolean Restart to run the game multiple times
    pygame.init()     
    hold_screen = True       ## to hold the screen untill a button is clicked
    font = pygame.font.Font("freesansbold.ttf", 25)
    
    while (restart_game):

        #########################
        ## High score management
        #########################
        file_highscore = shelve.open("Highscore.dat")
        #########################
        #########################
        

        ###########################################################
        ## Intro screen
        ###########################################################
        win = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Color challenege")
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        win.fill((255,255,255))
        label = font.render("Play!!", 1, (0,0,0))
        bg = pygame.image.load("pyimage.png")
        win.blit(bg, (0,0))
        pygame.draw.rect(win, (255,0,0), (330, 330, 150, 100))
        win.blit(label, (370, 370))
        pygame.display.flip()
        ###########################################################
        ###########################################################


        ###########################################################
        ## Holding screen untill play putton is clicked
        ###########################################################
        
        while (hold_screen):

             for event in pygame.event.get():
                 if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if mx > 350 and mx < 500 and my > 350 and my < 450:

                        hold_screen = False

        ###########################################################                 
        ## Creating an instance of Game class and playing sound
        ###########################################################
                        
        start_sound = pygame.mixer.Sound("JingleBells.wav")
        start_sound.play()
        game1 = Game(win)  ##instance of Game class 
        start_sound.stop()
        end_sound = pygame.mixer.Sound("Gameoversound.wav")
        end_sound.play()

        ###########################################################
        ## Highscore analysis
        if game1.get_score() > file_highscore["high_score"]:

            file_highscore["high_score"] = game1.get_score()
            
        file_highscore.sync()
        
        ###########################################################
        ## End Screen
        win.fill((255,255,255))
        win.blit(bg, (0,0))
        end_msg = "Your score: " + str(game1.get_score())  ##Printing your score
        label = font.render(end_msg , 1, (0,0,0))
        win.blit(label, (320, 280))
        pygame.display.flip()
        pygame.draw.rect(win, (0,255,0), (250, 350, 150, 100))
        end_msg2 = "Play again!!"       ##Play again button
        label = font.render(end_msg2, 1, (0,0,0))
        win.blit(label, (255, 380))
        end_msg2 = "Quit!!"             ##Quit button
        end_msg3 = "High score: " + str(file_highscore["high_score"])  ##Printing highscore
        label = font.render(end_msg3, 1, (0,0,0))
        win.blit(label, (320,250))
        pygame.draw.rect(win, (255,0,0), (450, 350, 150, 100))
        label = font.render(end_msg2, 1, (0,0,0))
        win.blit(label, (490, 380))
        pygame.display.flip()

        ###############################################################
        ## Holdind end screen until a button is pressed
        
        hold_screen = True
        while (hold_screen):
            
            for event in pygame.event.get():
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if mx > 250 and mx < 400 and my > 350 and my < 450:

                        restart_game = True
                        hold_screen = False
                
                    elif ((mx > 450 and mx < 600 and my > 350 and my < 450) or event.type == pygame.QUIT):
                        

                        restart_game = False
                        hold_screen = False
        ################################################################
                        
        file_highscore.close()      

    #######################################
    ## Game quiting if restart_game is false    
    pygame.quit()
    
    
####Kick-off
main()
