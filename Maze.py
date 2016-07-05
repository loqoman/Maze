''' Maze
                    '''

import pygame, sys, time, random,math
from pygame.locals import *

pygame.init()
''' Maze ver 0.1 - have the rat look for the cheeses using the arrow keys.
Scoring and controls not implemented yet nor does he know when he has found the
way out.  But you can pick up the cheeses.
If you want it to be hard, change ROOMS_V to 50 and see what happens.'''


BLACK = (0,0,0)
WHITE =  (255,255,255)
YELLOW = (255,255,0)
LIGHTYELLOW = (128,128,0)
RED = (255, 0 ,0)
LIGHTRED = (128,0,0)
BLUE = (0, 0, 255)
SKYBLUE = (135,206,250)
GREEN = (0,255,0)
LIGHTGREEN = (152,251,152)
AQUAMARINE = (123,255,212)
LIGHTBROWN = (210,180,140)
LIGHTGREY = (211,211,211)
DIMGREY = (105,105,105)
VIOLET = (238,130,238)
SALMON = (250,128,114)
GOLD = (255,165,0)
BACKGROUND = LIGHTGREY
WINDOWWIDTH = 1250
WINDOWHEIGHT = 750
MAZE_TOPLEFT = (50,150)   # Top left corner of the maze area
MAZE_WIDTH = 1000
MAZE_HEIGHT = 600

ROOMS_V =30  # number of rooms in the vertical direction
ROOMS_H = int(ROOMS_V * (float(MAZE_WIDTH)/float(MAZE_HEIGHT)))
SIZE = int(float(MAZE_HEIGHT)/float(ROOMS_V))
STARTING_COL = 0
STARTING_ROW = int(ROOMS_V/2)

windowSurface = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption('Maze')

#--------------------Maze Class -----------------------------------------
# Class for the maze
class Maze(object):
#



    def __init__(self):
    # Maze initialization method called when maze is created

        
        return  # return from Maze.__init__

    def build(self):
    # Maze.build function called at the Maze object level to build a maze.


        # Fill in the rooms array with the room objects
        for h in range (0,ROOMS_H):
            Room.rooms.append([])  # this creates the second dimension
            for v in range(0,ROOMS_V):
                room = Room(size=SIZE,row=v,col=h)
                Room.rooms[h].append(room)
                Room.unused_rooms.append(room)
        
        # generator doesn't mark the starting room because it is used for branches
        # so mark the starting room as solid white



        while True:
            room = Room.rooms[STARTING_COL][STARTING_ROW]
            room.room_color = WHITE
            room.state = 'P'
            Room.draw(room)

            # Do a random walk for primary path
            p_path = Path() # create an object for the primary path
            east_exit = p_path.random_walk(col=STARTING_COL,row=STARTING_ROW,
                                    color=RED,room_state='P',seek_east=True)
            if east_exit:
                break
            else:
                Maze.reset(maze) # reset the array and try again

        room = Room.rooms[STARTING_COL][STARTING_ROW]
        Room.unused_rooms.remove(room)
        p_path.rooms.insert(0,room)  # add starting room to head of rooms list

        Path.primary_path.append(p_path) # append the path object, only one

        # Now build some secondary paths
        for i in range(0,int(len(p_path.rooms)/5)):
            room_index = random.randrange(0,len(p_path.rooms))
            room = p_path.rooms[room_index]
            col = room.col
            row = room.row
            s_path = Path()  # create a new secondary path object
            unused = s_path.random_walk(col,row,color=YELLOW,
                                         room_state='S')
            if len(s_path.rooms) > 0: # don't store empty path
                Path.level2_paths.append(s_path)
            
        # Also build some Tertiary paths]
        if len(Path.level2_paths) >0:  # make sure there are paths at level 2
            for i in range(0,len(Path.level2_paths)): # for all paths in level2
                
                if len(Path.level2_paths[i].rooms) > 0: # insure some rooms
                    for j in range(0,int(len(Path.level2_paths[i].rooms))):
                        room_index = random.randrange(0,
                                            len(Path.level2_paths[i].rooms))
                        room = Path.level2_paths[i].rooms[room_index]
                        col =room.col
                        row =room.row
                        t_path = Path()   # ceate a new path object
                        unused= t_path.random_walk(col,row,color=GREEN,
                                                 room_state='T')
                        if len(t_path.rooms) > 0: # don't store empty path
                            Path.level3_paths.append(t_path)
        # And finally some level4 paths
        if len(Path.level3_paths) >0:  # make sure there are paths at level 3
            for i in range(0,len(Path.level3_paths)): # for all paths in level 3
                if len(Path.level3_paths[i].rooms) > 0: # ensure some rooms
                    for j in range(0,int(len(Path.level3_paths[i].rooms))):
                        room_index = random.randrange(0,
                                            len(Path.level3_paths[i].rooms))
                        room = Path.level3_paths[i].rooms[room_index]
                        col =room.col
                        row =room.row
                        f_path = Path()  # create a new path object
                        unused= f_path.random_walk(col,row,
                                                color=AQUAMARINE,
                                                 room_state='F')
                        if len(f_path.rooms) > 0: # don't store empty path
                            Path.level4_paths.append(f_path) 
           
        # For debug, turn all the unused rooms to a light color

        for i in range(0,len(Room.unused_rooms)):
            room = Room.unused_rooms[i]
            room.room_color = LIGHTGREY
            Room.draw(room)

        # clean up the unused cells

        while len(Room.unused_rooms) > 0:
            # select an unused room to start a dead end path
            room = random.choice(Room.unused_rooms)
        #    print('calling dead_end',room.col,room.row)
        #    print('length of unused rooms is',len(Room.unused_rooms))
#            d_path = Path()
            d_path = Path()    # build a new path object
            status = d_path.build_dead_end(room.col,room.row,
                                            color=SALMON,room_state='D')
            if status:
                Path.dead_end_paths.append(d_path)
            
        time.sleep(5)

        # Show maze in light color
        for col in range(0,ROOMS_H):
            for row in range(0,ROOMS_V):
                room = Room.rooms[col][row]
                room.room_color = LIGHTGREY
                room.draw()

        # Redraw the starting room in white
        room = Room.rooms[STARTING_COL][STARTING_ROW]
        room.room_color = WHITE
        room.draw()
        pygame.display.update()
        
        # return from Maze.build
        return  

    def reset(self):
    # Maze method to reset the room array to initial condition
        Room.unused_rooms = []  # empty the unused rooms list
        for col in range (0,ROOMS_H):
            for row in range(0,ROOMS_V):
                room = Room.rooms[col][row]
                Room.unused_rooms.append(room)
                room.room_color = BACKGROUND
                room.state = None;
                room.contents = []  # reset to no contents
                #initialize the state of the walls, True means they are up
                room.n_wall = True
                room.s_wall = True
                room.e_wall = True
                room.w_wall = True
                room.draw()

        return # return from Maze.reset

#------------------- Path Class ----------------------------------------
# Class for paths through the maze
class Path(object):
    primary_path = [] # the primary path object in list same as others
    level2_paths = [] # the list of paths that are secondary
    level3_paths = [] # list of the third level paths
    level4_paths = [] # list of fourth level paths
    dead_end_paths = [] # list dead end paths randomly connected to others
    '''
     N
     |
 W---|---E
     |
     S
    '''
    def __init__(self):
    # Path class initializer, called when a path is created to build path object                        
        self.rooms = [] # set the rooms list empty

        return  # return from Path.__init__

    def random_walk(self,col=0,row=0,color=BACKGROUND,room_state='P',
                    seek_east=False):
    # Function to do a random walk
#        self.rooms.append(Room.rooms[col][row])
        while True:
            old_col = col
            old_row = row
            # try a random direction out and see if we can move there
            possible_directions=['N','S','E','W']
            if seek_east:
               possible_directions=['N','N','S','S','E','E','E','W']            
            if seek_east:
                if (row == 0) |(row >= ROOMS_V-1): # don't loop back if N or S
                    possible_directions.remove('W')
            while len(possible_directions) > 0:
                room = Room.rooms[col][row]

                try_index = random.randrange(0,len(possible_directions))

    #           print(try_index,col,row,possible_directions)       
                direction = possible_directions[try_index]
                del possible_directions[try_index]
                status,col,row = Room.walk(room,
                                           direction=direction,wall_check=False)
    #           print('Room state is ',Room.rooms[col][row].state)
                if ((not status) |
                    (not (Room.rooms[col][row].state == None)) ):
                    col = old_col  # room was busy, back out
                    row = old_row
                    if len(possible_directions) <= 0: # we are stuck
                        return False     # return no east exit
                    
                else:  # room seems OK to add to the walk

                   # get the object for this room and change its color as indicated
                    old_room = Room.rooms[old_col][old_row]  # remember old room to knock down its walls
                    room = Room.rooms[col][row]
                    self.rooms.append(room)
                    room.room_color = color
                    room.state = room_state  # indicate room is used
                    Room.unused_rooms.remove(room)  # delete from unusued rooms
                    # knock down the wall in old and new room.
                    Room.knock_out_walls(direction,room,old_room)    
                    
                    if seek_east and (col == ROOMS_H-1):

                        return True # we found an east exit
                    else:
                        break
    #        time.sleep(.1)
                 

        return False  # shouldn't ever get here.

    def build_dead_end(self,col=0,row=0,color=LIGHTGREEN,room_state='D'):
    # Function to do clear out unused rooms by building dead end paths.  They
    # break into any exiting path that is not isolated from another path.
    # call with a row and column on the unused room list.
    # returns with status (False if stuck) and new deadend path.
    # note deadend paths start at the end room.

        search = [] # this will hold tuples for rooms and directions entered
        # pick out an unused room and start there
        room = Room.rooms[col][row]  # start with the indicated room
        search.append((room,None))  # remember room and entry direction
        room.state = 'X'   # indicate we are in search mode
        room.room_color= LIGHTGREEN # show in search path
        room.draw()
        while True:
            old_col = col
            old_row = row
            # try a random direction out and see if we can move there
            possible_directions=['N','S','E','W']

            while (len(possible_directions) > 0) :
                room = Room.rooms[col][row]

                try_index = random.randrange(0,len(possible_directions))

#                print(try_index,col,row,possible_directions)       
                direction = possible_directions[try_index]
                del possible_directions[try_index]
                status,col,row = Room.walk(room,
                                           direction=direction,wall_check=False)
#                print('Trial room is ',col,row,Room.rooms[col][row].state)
                if ((status) and
                    (Room.rooms[col][row].state != 'X') ): # don't loop on itself

#                    print('room seems ok')                
                    # Room seems OK
                    # get the object for this room 
                    old_room = Room.rooms[old_col][old_row]  # remember old room
                    room = Room.rooms[col][row]


                    if room.state != None:
                        # knock out the wall into this room
                        Room.knock_out_walls(direction,room,old_room)
#                        print('found a way out',room.col,room.row,room.state)
                        # Found another path, this is out way out
                        # walk search path, fixing status,color and clearing walls

#                        print ('len(search),first entry=',len(search),search)
                        while len(search) > 0:
                            entry = search[0] # get from head of list
                            room = entry[0]
                            self.rooms.append(room)
                            direction = entry[1]
#                            print ('from search',room.col,room.row,room.state,direction)
                            room.state = room_state # indicate on dead end path
                            room.room_color = color # set to argument color
                            room.draw()
                            pygame.display.update()
                            if direction != None: # bypass first room
                                Room.knock_out_walls(direction,room,old_room)
                                old_room.draw()
                                room.draw()
                                old_room = room
                            else:  # it is the first room
                                old_room.room_color = color
                                old_room.draw()
                                old_room = room

                            Room.unused_rooms.remove(room)
                            search.remove(entry) # trim down the temp list

#                        print('connected to another path exiting with true status')
                        return True  # return Ok


                                    
                    else:  # room OK,but still searching
    #                    print('room ok but still searching')
                        room.room_color = LIGHTBROWN
                        room.state = 'X'  # indicate room is used in search
                        search.append((room,direction)) # room and way we came in
                        Room.draw(room)
                        break
               
                else:  # Can't go this way or use this room
    #                print('cant go this way or use this room')
                    room.room_color = LIGHTGREEN # for debug set to lightgreen
                    col = old_col  # room was busy, back out
                    row = old_row
                    if len(possible_directions) <= 0: # we are stuck
                        # we are stuck, walk the path and reset status to unused.
                        while len(search) > 0:
                            for entry in search:
    #                            print('we are stuck,len search=',len(search))
                                room = entry[0]  # get the room
                                room.state = None # set back to unused
                                room.room_color = BACKGROUND # for debugging visuals
                                Room.draw(room)
                                search.remove(entry)
    #                    print('exiting with false status')
                        return False
                    

#            time.sleep(.1)
                 
        print('build dead end - tilt, shouldnot get here')
        return False  # shouldn't ever get here.



#------------------- Room Class  ----------------------------------------
#Class for the rooms in the maze
class Room(object):
    
    rooms = []  # holds the doubly indexed list of room objects
    unused_rooms = [] # single indexed list of the unused rooms
    
    def __init__(self,size=20,row=0,col=0):
    #Room initialization method called when room is created.  Column and row
    # give the position in the array
        self.room_color = BACKGROUND  # chose the paint colors
        self.wall_color = BLACK
        self.size = size  # size of the room in pixels
        self.col = col    # column coordinate
        self.row = row   # row coordinate
        self.state = None   # usage state of the room
        self.contents = [] # contents list to empty

        #initialize the state of the walls, True means they are up
        self.n_wall = True
        self.s_wall = True
        self.e_wall = True
        self.w_wall = True

        #define a rectangle for this room and save it
        left = int(float((WINDOWWIDTH-MAZE_WIDTH)/2.)
                   +int(self.col*float(size)))
        top =  int(float((WINDOWHEIGHT-MAZE_HEIGHT)/2)
                   +int(self.row*float(size)))
        self.rect = pygame.Rect(left,top,size,size)

        self.draw()  # draw the room

        return  # return from Room.__init__

    def draw(self):
    # Room method to draw and room and it's walls acording to current wall state

        pygame.draw.rect(windowSurface,self.room_color,self.rect,0) # draw the floor

        #draw the walls based on their state
        if self.n_wall:
            pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.left,self.rect.top),
                             (self.rect.left+self.size,self.rect.top),1)
        if self.s_wall:
           pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.left,self.rect.bottom),
                             (self.rect.left+self.size,self.rect.bottom),1)
        if self.w_wall:
           pygame.draw.line(windowSurface,self.wall_color,
                 (self.rect.left,self.rect.top),
                 (self.rect.left,self.rect.top+self.size),1)
        if self.e_wall:
           pygame.draw.line(windowSurface,self.wall_color,
                             (self.rect.right,self.rect.top),
                             (self.rect.right,self.rect.top+self.size),1)
        

        pygame.display.update()

        return  # return from Maze.draw

    def walk(self,direction='N',wall_check=True):
    #Maze method to walk out of a room
    # if walk_check is False, you can walk through walls (used for initial
    # maze setup). Returns false if we can't go that way, also returns updated
    # room object.
    
        moved = False  # establish default
        col = self.col # initial col
        row = self.row
        if ( (direction == 'N') &
             (self.row >0) ):
            if( (not self.n_wall) |  (not wall_check)):
                 row -=1
                 moved = True
        if ( (direction == 'S') &
             (self.row < (ROOMS_V-1) ) ):
            if( (not self.s_wall) |  (not wall_check)):
                 row +=1
                 moved = True
        if ( (direction == 'W') &
             (self.col >0) ):
            if( (not self.w_wall) |  (not wall_check)):
                 col -=1
                 moved = True
        if ( (direction == 'E') &
             (self.col < (ROOMS_H-1) ) ):
            if( (not self.e_wall) |  (not wall_check)):
                 col +=1
                 moved = True
#        print('dir,N,S,E,W= ',direction,self.n_wall,self.s_wall,
#              self.e_wall,self.w_wall)

        return moved,col,row  # returned with indication of success or failure

    def knock_out_walls(direction,room,old_room):
    # General purpose function to clear the walls from which we entered a room.
    # direction is the direction we were going when we entered.
    # room is current room object. old_room is the room we entered from.
 

        if direction == 'N':
            old_room.n_wall = False
            room.s_wall = False
        elif direction == 'S':
            old_room.s_wall = False
            room.n_wall = False
        elif direction == 'E':
            old_room.e_wall = False
            room.w_wall = False
        elif direction == 'W':
            old_room.w_wall = False
            room.e_wall = False
        Room.draw(old_room) # redraw both rooms
        Room.draw(room)

        return # return from knock_out_walls
#---------------------- Rat Class ----------------------------------------
# Rat class for the rat that is going to run the maze
class Rat(object):  # create Rat object

    def __init__(self,direction = 'E',color=DIMGREY ):

        self.direction = direction
        self.color = color
        self.room = Room.rooms[STARTING_COL][STARTING_ROW]
        self.cheeses = []  # empty list of cheeses we carrys

        self.draw()  # draw him in the starting room
        
        return # return from Rat.__init__

    def draw(self):
    # draw the rat in his room

        pygame.draw.circle(windowSurface,self.color,self.room.rect.center,
                           int(self.room.size/3),0)
        pygame.display.update()

        return  # return from Rat.__init__

    def erase(self):
    # erase the rat from this room

        pygame.draw.circle(windowSurface,self.room.room_color,
                           self.room.rect.center,int(self.room.size/3),0)
        pygame.display.update()

        return # return from Rat.erase

    def move(self,direction='E'):
    # move the rat in the indicated direction
        status,col,row = self.room.walk(direction)
        if status: # move was legal
            self.erase()   # erase from the current room
            self.room = Room.rooms[col][row] # get new room he is in
            self.check_for_cheese(self.room)
            self.draw()   # draw rat in new room

        return status   # return whether move occurred or not

    def check_for_cheese(self,room):
    # see if there is cheese in room, if so, pick up cheese, change room color
    # to background and return true
        if 'cheese' in room.contents:
            self.cheeses.append('cheese')
            room.contents.remove('cheese')
            room.room_color = BACKGROUND
            self.room.draw() # redraw room with no cheese
            return True
        else:
            return False
                
#------------------------------------------------------------------
# Define the widget classes
#------------------------------------------------------------------

class Widget(object):
# Widget class for all widgets,  its  function is mainly to hold the
# dictionary of all widget objects by name as well as the application
# specific handler function. And support isclicked to
# see if cursor is clicked over widget.

    widgetlist = {} # dictionary of tubles of (button_object,app_handler)
    background_color = LIGHTGREY

    def __init__(self):
    # set up default dimensions in case they are not defined in
    # inherited class, this causes isclicked to default to False
        self.left = -1
        self.width = -1
        self.top = -1
        self.height = -1

    def find_widget(widget_name):
    # find the object handle for a widget by name        
        if widget_name in Widget.widgetlist:
            widget_object = Widget.widgetlist[widget_name][0]
            return  widget_object
        else:
            Print ('Error in find_widget, Widget not found ' + widget_name)
            return

    def isclicked (self, curpos):
    # button was clicked, is this the one? curpos is position tuple (x,y)
        

        covered = False

        if (curpos[0] >= self.left and
        curpos[0] <= self.left+self.width and
        curpos[1] >= self.top and
        curpos[1] <= self.top + self.height):
            covered = True

        return covered
    

    def handler(self):
    # prototype for a widget handler to be overridden if desired
        pass     
            
class Button(Widget):

    buttonlist = []
    grouplist = {}
    
    def __init__ (self, window = windowSurface,color = BLACK,
                  topleft = (200,200), size=20,name = '', label='',
                  value = '',app_handler=Widget.handler,
                  group = '',groupaction = 'RADIO'):   

        self.window = window
        self.color = color
        self.topleft = topleft
        self.left = topleft[0]  # required by isclicked method in Widget
        self.top = topleft[1]   # "
        self.width = size       # "
        self.height = size      # "
        self.right = self.left + size
        self.bottom = self.top + size
        self.size = size
        self.name = name
        self.label = label
        self.value = value
        self.app_handler = app_handler # object of applications specific handler
        self.group = group
        
        self.groupaction = groupaction
        # groupaction value of 'RADIO' allows only one in group to be on
        # 'RADIO_WITH_OFF' allows only one but all off also
        # '' means no group action required

        self.state = False    # Initialize button state to 'off'


        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        else:
            print ('Error - duplicate widget name of ' + name)

        Button.buttonlist += [self] # add to button list as a object

        # if button is in a group, add group to dictionary if the group is not
        # already there.  Then add the button to the group.

        if group in Button.grouplist:
            Button.grouplist[group] += (self,)
        else:
            Button.grouplist[group] = (self,)


        
        # get the rectangle for the object
        self.rect = pygame.draw.rect(window,color,
        (topleft[0],topleft[1],size,size),1)

        #write label if any
        if label != '':
           self._label()
            
        self.draw()

    def _label(self): # private method to generate label, does not do draw
       labelFont = pygame.font.SysFont(None, int(self.size*1.5) )
       text = labelFont.render(self.label,True,self.color,
       Widget.background_color)
       
       textRect= text.get_rect()
       textRect.left = self.rect.right + 5
       textRect.bottom = self.rect.bottom
       self.window.blit(text, textRect)
                                                   

    def identify(self):  # print my name
        print ("Button name is:" + self.name)

    def draw (self): # draw button with current state
        
        self.rect = pygame.draw.rect(self.window, self.color,
        self.rect,1)

        if self.state:

            pygame.draw.circle(self.window,self.color,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2))
            ,int(self.size/2)-2,0)
        else:
            pygame.draw.circle(self.window,WHITE,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2)),
            int(self.size/2)-2,0)
            
            pygame.draw.circle(self.window,self.color,
            (self.rect.left+int(self.size/2),self.rect.top+int(self.size/2)),
            int(self.size/2)-2,1)
                               
        pygame.display.update()   # refresh the screen

    def toggle (self):  # toggle the button state
        if self.state:
            self.state = False
        else:
            self.state = True
            
        self.draw()



    def group_handler(self):
    # if button in a group, button is now on and is a RADIO button  then
    # turn off all other buttons in the group

        #if groupaction is 'RADIO' or 'RADIO_WITH_OFF'and new state is on,
        # turn off all other buttons in the group. 
        if ( (self.groupaction == 'RADIO') |
             (self.groupaction == 'RADIO_WITH_OFF') ):

            # loop finding other buttons in group and turning them off
            for i in range(len((Button.buttonlist))):

                if (Button.buttonlist[i].group == self.group and
                Button.buttonlist[i] != self):
                    Button.buttonlist[i].state = False
                    Button.draw(Button.buttonlist[i])

        # Now, if 'RADIO' and if new state is off,
        # tun it back on because at least one must be on in the group.
        if self.groupaction == 'RADIO':
            if (self.state == False):
                self.toggle()
                return
#------------------------------------------------------------
# Button handler method,  overriding the Widget
# handler method prototype. Does some general work then calls the
# group handler and application specific handler if any
#------------------------------------------------------------

    def handler(self):


        # toggle the state of the button
        self.toggle()

        # see if button is in a group and if so, call  the group handler
        # in button class to enforce such things as 'RADIO' exclusivity
        if self.group != '':
            self.group_handler()

        # call the application specific handler (if none specified when
        # button is created it defaults to dummy prototype Widget.handler).
        self.app_handler(self)


        return
             

class Text(Widget):

    def __init__(self,window=windowSurface,
                 color=BLACK,background_color=Widget.background_color,
                 topleft=(200,200),name= '',
                 font_size=20,max_chars=20,text='',
                 outline=True,outline_width=1,
                 justify = 'LEFT',
                 app_handler=Widget.handler):

        
        # initialize the properties
        self.window=window
        self.color= color
        self.background_color = background_color
        self.name = name
        self.font_size = font_size
        self.max_chars = max_chars
        self.text = text
        self.outline = outline
        self.outline_width = outline_width
        self.justify = justify
        self.app_handler = app_handler
        
        self.topleft=topleft
        self.left=topleft[0]    # reguired by isclicked method in Widget
        self.top=topleft[1]     # "
        
        # render a maximum size string to set size of text rectangle
        max_string = ''
        for i in range(0,max_chars):
            max_string += 'D'

        maxFont = pygame.font.SysFont(None,font_size)
        maxtext = maxFont.render(max_string,True,color)
        maxRect= maxtext.get_rect()
        maxRect.left = self.left
        maxRect.top = self.top
        self.maxRect = maxRect  # save for other references
        self.maxFont = maxFont

        # now set the rest required by isclicked method
        self.width = maxRect.right - maxRect.left
        self.height = maxRect.bottom -  maxRect.top


        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        elif (name != ''):
            print ('Error - duplicate widget name of ' + name)

        self.draw()  # invoke the method to do the draw

        return   # end of Text initializer

    # Text method to draw the text and any outline on to the screen
    def draw(self):
        # fill the maxRect to background color to wipe any prev text
        pygame.draw.rect(self.window,self.background_color,
                         (self.maxRect.left,self.maxRect.top,
                          self.width, self.height),0)

        # if outline is requested, draw the outline 4 pixels bigger than
        # max text.  Reference topleft stays as specified
        
        if self.outline:
            pygame.draw.rect(self.window,self.color,
                             (self.maxRect.left-self.outline_width-2,
                              self.maxRect.top-self.outline_width-2,
                              self.width+(2*self.outline_width)+2,
                              self.height+(2*self.outline_width)+2),
                              self.outline_width)


        # Now put the requested text within maximum rectangle
        plottext = self.maxFont.render(self.text,True,self.color)
        plotRect = plottext.get_rect()

        plotRect.top = self.top # top doesn't move with justify

        # justify the text
        if self.justify == 'CENTER':
            plotRect.left = self.left + int(plotRect.width/2) 
        elif self.justify == 'LEFT':
            plotRect.left = self.left
        elif self.justify == 'RIGHT':
            plotRect.right = self.maxRect.right
        else:
            print('Illegal justification in Text object ',self.justify, end='\n')

        # blit the text and update screen
        self.window.blit(plottext,plotRect)

        pygame.display.update()

    # Text method to update text and redraw
    def update(self,text):
        self.text = text
        self.draw()

class Rectangle(Widget):
# class to wrap the pygame rectangle class to standardize with Widgets 

    def __init__(self, window=windowSurface,color=BLACK,
                 topleft = (200,200), width = 30, height = 20,
                 name = '',outline_width = 1, # width of outline, 0 = fill
                 app_handler=Widget.handler):

        self.window = window
        self.color = color
        self.topleft = topleft
        self.left = topleft[0]      # required by isclicked method in Widget
        self.top = topleft[1]       # "
        self.width = width          # "
        self.height = height        # "
        self.right = self.left + width
        self.bottom = self.top + height
        self.name = name
        self.outline_width = outline_width
        self.app_handler = app_handler

        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        elif (name != ''):
            print ('Error - duplicate widget name of ' + name)

        self.draw()  # invoke the draw method to draw it

        return

    def draw(self):     # Rectangle method to do the draw
        
        # get a rectangle object and draw it
        self.rect = pygame.Rect(self.left,self.top,self.width,self.height)
        pygame.draw.rect(self.window,self.color,self.rect,
                         self.outline_width)
        pygame.display.update(self.rect)

        return
    
    def handler(self):  # Rectangle handler
        self.app_handler(self)  # nothing special to do, call app_handler
        return
    


#---------------- General purpose functions not part of a class ver 0.1 ---------



def check_wall(rect):
# General purpose function to test if an  hit a wall.
# Call with a rectangle object
# Returns None if no wall struck, otherwise 'TOP','BOTTOM','RIGHT','LEFT'
    if (rect.right >= WINDOWWIDTH):
        return 'RIGHT'
    elif (rect.left <= 0):
        return 'LEFT'
    elif (rect.top <= 0):
        return 'TOP'
    elif (rect.bottom >= WINDOWHEIGHT):
        return 'BOTTOM'
    else:
        return None




def write_text(text='TEXT TEST',topleft=(200,200),font_size=50,color=YELLOW):
# General purpose function to write text on the screen
    myfont = pygame.font.SysFont(0,font_size)#setting for the font size
    label = myfont.render(text, 1,color)#("text",alias flag, color
    textrec = label.get_rect()  # get a rectangle to put it in
    textrec.left = topleft[0]  # set the position
    textrec.top = topleft[1]

    windowSurface.blit(label,textrec)#put the text rec onto the surface
    pygame.display.update()

    return  # end of write text

    return # return from update scores

#-------------Application specific setup functions not part of a class ------


def store_cheese(num_cheeses= 10):
# store cheese in the longest paths of level 4 paths

    num_stored = 0    
        # find the longest path not already used
    path_used = []
    while num_stored < num_cheeses:
        longest_path = 0
        most_rooms = 0
        for path_index in range(0,len(Path.level4_paths)):
            if ( (len(Path.level4_paths[path_index].rooms) > most_rooms) and
                 (path_index not in path_used) ):
                 longest_path = path_index
                 most_rooms = len(Path.level4_paths[path_index].rooms)

        path_used.append(longest_path) # use longest path not yet used           
        path =Path.level4_paths[longest_path]
        room = path.rooms[len(path.rooms)-1]
        room.room_color = GOLD
        room.contents.append('cheese')
        room.draw()
        num_stored += 1
        pygame.display.update()
    return  # return from store cheeese

def init_controls():
# Initialize the game controls and scoreboard widgets

    go = Button(name='Go',color = RED,topleft=(10,10),size = 35, #Big GO button at the top
                label='Go')

    player1 = Button(name='Player1',color=RED,
                     topleft =(WINDOWWIDTH-int(WINDOWWIDTH/3),10),size = 20,
                     label='Player 1',group='Player')
    
    player1.toggle() # set default to player 1 to True

    player1_score=Text(color=RED,topleft=(player1.right+100,player1.top),
                       name='player1_score',font_size=30,max_chars=20,
                       text='Best time',justify='LEFT',outline=False)
                                          

    player2 = Button(name='Player2',color=BLUE,
                     topleft =(player1.left,player1.bottom+10),size = 20,
                     label='Player 2',group='Player')
    player2_score=Text(color=BLUE,topleft=(player2.right+100,player2.top),
                       name='player2_score',font_size=30,max_chars=20,
                       text='Best time',justify='LEFT',outline=False)

    clock = Text(color=BLACK,topleft=(int(WINDOWWIDTH/2-300),10),
                  name='clock',font_size=40,max_chars=20,text='Elapsed time',  #Clock area at the top
                  justify='LEFT',outline=True)
    
    #Following are the difficulty buttons
    dif_easy = Button(name ='Easy',color = RED,
                      topleft=(10,75),size = 15,
                      label='Easy',group='Difficulty')

    dif_harder = Button(name ='Harder',color = RED,
                      topleft=(10,dif_easy.bottom+10),size = 15,
                      label='Harder',group='Difficulty')

    dif_harder.toggle() # set default difficulty to 'Harder'

    tough = Button(name ='Tough',color = RED,
                      topleft=(10,dif_harder.bottom+10),size = 15,
                      label='Tough',group='Difficulty')

    dig_worst = Button(name='Horrible',color=RED,
                       topleft=(10,tough.bottom+10),size = 15,
                       label='Horrible',group='Difficulty')

    new = Button(name ='New',color=RED,
                 topleft=(10,dig_worst.bottom+20),size=15,
                 label='New maze')
    return


#---------------End of general purpose functions --------------------#           
#---------------Button Applications handlers-------------------------#
def go_application_handler():
    #Start timer <Code>
    return
    #

#----------------Main portion of the program ver 0.2 --------------------
# Initialize things before the loop
pygame.key.set_repeat(50,50)
init_controls()
maze = Maze()

#Waiting for the user to click the 'go' button

        
#  Main game loop, runs until window x'd out or someone wins

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type is KEYDOWN:

            key = pygame.key.name(event.key)

            if(key == 'D'):
                rat.move('E')
            elif(key == 'down'): 
                rat.move('S')
            elif(key == 'A'):
                rat.move('W')
            elif(key == 'W'):  
                rat.move('N')
        if event.type == MOUSEBUTTONDOWN:                
                for widgetname in Widget.widgetlist: #For every widget we have ever created

                    widget_object = Widget.find_widget(widgetname) #Temp varible for the widget name 
                    pos = pygame.mouse.get_pos() # mouse clicked get (x, y)

                    if widget_object.isclicked(pos): #isclicked, to see if something is clicked.

                        widget_object.handler()#Well, its clicked, so do the self.handler()
      
        

    pygame.display.update()
    time.sleep(.02)


sys.exit() # shouldn't ever get here.  Exit is in main loop.
        

