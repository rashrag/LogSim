import pygame
import sys
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
screen = pygame.display.set_mode([1000,600])
img="dummy.jpg"
d={'and':'and.png',"":'dummy.png','or':'or.png','nor':'nor.png','not':'not.png','nand':'nand.png','xor':'xor.png','delete':'DELETE.jpg'}
gates_dict = dict()
gate_counter = 0
graph = []

#class to create gates
class Gates(pygame.sprite.Sprite):
    def __init__(self,gate):
         pygame.sprite.Sprite.__init__(self)
         self.gatetype=gate
         self.noneexists = False
         global d, all_sprites, gates_dict, gate_counter, points_list, graph
         img = pygame.image.load(d[gate])
         self.image = img.convert()
         self.image.set_colorkey(white)      
         self.rect = self.image.get_rect()
         if(gate!='not'): # because all other gates have two sockets
             for i in range(len(gates_dict)):
                 if gates_dict[i] == None:
                     gates_dict[i] = self
                     self.noneexists = True
                     break
                    
             if(self.noneexists == False):
                 gates_dict[gate_counter] = self
                 
             gate_counter += 1
             self.inputSockets = [Socket('in', self), Socket('in', self)]
             self.outputSocket = Socket('out', self)
             
         elif(gate=='not'):
             gates_dict[gate_counter] = self
             gate_counter += 1
             self.inputSockets = [Socket('in',self)]
             self.outputSocket = Socket('out',self)

    def draw_socket(self):
        # to draw sockets on each input and output of the gate
        if(self.gatetype != 'not'):
            self.inputSockets[0].rect.x = (self.rect.x)-1
            self.inputSockets[0].rect.y = (self.rect.y)+12
            all_sprites.add(self.inputSockets[0])
            socket_list.add(self.inputSockets[0])
            self.inputSockets[1].rect.x = (self.rect.x)-1
            self.inputSockets[1].rect.y = (self.rect.y)+33
            all_sprites.add(self.inputSockets[1])
            socket_list.add(self.inputSockets[1])
            self.outputSocket.rect.x = (self.rect.x)+95
            self.outputSocket.rect.y = (self.rect.y)+22
            all_sprites.add(self.outputSocket)
            socket_list.add(self.outputSocket)
        else:
            self.inputSockets[0].rect.x = self.rect.x-1
            self.inputSockets[0].rect.y = self.rect.y+22
            all_sprites.add(self.inputSockets[0])
            socket_list.add(self.inputSockets[0])
            self.outputSocket.rect.x = self.rect.x+90
            self.outputSocket.rect.y = self.rect.y+22
            all_sprites.add(self.outputSocket)
            socket_list.add(self.outputSocket)
                        

    def get_input_values(self): # get input values from the sockets
        if(self.gatetype!='not'):
            self.in_val1 = self.inputSockets[0].val
            self.in_val2 = self.inputSockets[1].val
        else:
            self.in_val1 = self.inputSockets[0].val

    def set_output_values(self): # set output value to the socket
        self.out.val = 0
        self.outputSocket.val = self.out.val

    def delete(self):
        global gate_counter, gates_dict
        print('CAME HERE')
        for i in self.outputSocket.outgoing:
            i.incoming = None
            i.connected = False
        for i in self.inputSockets:
            if(i.incoming!=None):
                i.incoming.outgoing.remove(i)
        for i in lines:
            for j in i:
                xo = self.outputSocket.rect.x
                yo = self.outputSocket.rect.y
                xi1 = self.inputSockets[0].rect.x
                yi1 = self.inputSockets[0].rect.y
                xi2 = self.inputSockets[1].rect.x
                yi2 = self.inputSockets[1].rect.y
                xorange = [xo+i for i in range(-2,3,1)]
                yorange = [yo+i for i in range(-2,3,1)]
                xi1range = [xi1+i for i in range(-2,3,1)]
                yi1range = [yi1+i for i in range(-2,3,1)]
                xi2range = [xi2+i for i in range(-2,3,1)]
                yi2range = [yi2+i for i in range(-2,3,1)]
                
                if(j[0] in xorange or j[1] in yorange):
                    print('FOUND!!!!')
                    i.pop()
                    i.append(white)
                if(j[0] in xi1range or j[1] in yi1range):
                    print('FOUND!!!!')
                    i.pop()
                    i.append(white)
                if(j[0] in xi2range or j[1] in yi2range):
                    print('FOUND!!!!')
                    i.pop()
                    i.append(white)
                    
        self.gateindex = None
        
        for i in range(len(gates_dict)):
            if gates_dict[i] == self:
                gates_dict[i] = None
                self.gateindex = i
                print(self.gateindex)

        for i in range(len(graph)):
            graph[i][self.gateindex] = 0
            print (i)
            if(i==self.gateindex):
                graph[i] = [[0]*len(graph[i])]
                print(graph[i])
        print(graph)
                    

        gate_counter -= 1
        
        socket_list.remove(self.outputSocket)
        socket_list.remove(self.inputSockets[0])
        socket_list.remove(self.inputSockets[1])
        all_sprites.remove(self.outputSocket)
        all_sprites.remove(self.inputSockets[0])
        all_sprites.remove(self.inputSockets[1])
        all_gates.remove(self)
        all_sprites.remove(self)
        

class Socket(pygame.sprite.Sprite):
    def __init__(self, sock_type, bel_gate):
        global gates_dict
        pygame.sprite.Sprite.__init__(self)
        self.socket_type = sock_type
        self.val = None   # value of input or output is passed to gate through this
        self.belongs = None # to tell which gate this socket belongs to
        for i in range(len(gates_dict)):
            if gates_dict[i] == bel_gate:
                self.belongs = i
                break
            
        self.connected = False # check if there's already a connection to this socket. needed for inputs because you can't have multiple inputs
        self.outgoing = [] # to allow multiple output lines
        self.incoming = None # to check which socket it's connected from

        # draw the socket
        
        self.img = pygame.image.load('socket2.jpg')
        self.image = self.img.convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        
# for the initial switch for user input  
class Switch(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.output = Socket('out',self)
        self.val = 0
        img = pygame.image.load('switch0.bmp')
        self.image = img.convert()
        self.image.set_colorkey(white)      
        self.rect = self.image.get_rect()

    def draw_socket(self): # no input sockets for switches
        self.output.rect.x = self.rect.x + 60
        self.output.rect.y = self.rect.y+17
        all_sprites.add(self.output)
        socket_list.add(self.output)
        print(self.output.belongs)
        
    def change_output(self): # set switch to on or off when clicked
        self.val = int(not self.val)
        if(self.val == 0):
            img = pygame.image.load('switch0.bmp')
        else:
            img = pygame.image.load('switch1.bmp')
        self.image = img.convert()
        self.image.set_colorkey(white)
        self.set_output_values()

    def delete(self): # delete the switch
        global all_sprites, socket_list
        socket_list.remove(self.output)
        all_sprites.remove(self.output)
        all_sprites.remove(self)

    def set_output_values(self): # transfer output value of switch to it's output socket
        self.output.val = self.val
        for i in self.output.outgoing:
            i.val = self.val

clickedgate=""


# Class to create buttons
class Button(pygame.sprite.Sprite):

    # Constructor. takes colour, width, height, text of button
    def __init__(self, img, otherimg,gatename):
        # Call parent class constructor
        pygame.sprite.Sprite.__init__(self)
        self.clicked = False #initially, all buttons created are not clicked.
        self.change = otherimg
        self.original = img
        # Create a button and fill it with a colour.
        self.image = img.convert()
        self.image.set_colorkey(white)
        # Fetch the rectangle with the dimensions of the image. Set position by using rect.x, rect.y
        # Coordinates to put the button at and accessing those coordinates knowing the size will also be easy.
        self.rect = self.image.get_rect()
        self.gatename=gatename

    # make button look like it's been selected
    def change_colour(self, flag): 
        x = self.rect.x
        y = self.rect.y
        global text
        global clickedgate
        print(clickedgate)
        if(flag == False):
            self.image = self.change.convert()
            clickedgate=self.gatename
            text = clickedgate.upper()+" gate selected."
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = self.original.convert()
            clickedgate = ""
            text = 'Select a gate'
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    
            
event=pygame.event.poll()
pos1=(30,30)
socket_clicked = False
points_list=[]
lines = []
socket1 = None
socket2 = None
button_clicked = False
mouse_click_points = []
delete_set = False

# mouse click handler

def check_button(user):
    global pos1, points_list, socket_clicked, socket_selected, graph, button_clicked, socket1, socket2, socket_list, mouse_click_points, delete_set, all_gates, text
    hit = pygame.sprite.spritecollide(user, buttons_list, False)
    sock = pygame.sprite.spritecollide(user, socket_list, False)
    others = pygame.sprite.spritecollide(user, all_gates, False)
    print('here again')
    print(len(gates_dict))

    for i in socket_list:
        print(i.val)
    
    if(len(hit)!=0):
        if(clickedgate != "" and hit[0].gatename != clickedgate):
            text = 'Unselect previously selected button first'
        else:
            hit[0].change_colour(hit[0].clicked)
            button_clicked = not(button_clicked)
            hit[0].clicked = not(hit[0].clicked)
            if(hit[0].gatename == 'delete'):
                delete_set = not(delete_set)
        
    elif(len(sock)!=0): # check if socket was clicked
        print('before socket')
        socket_clicked = not (socket_clicked)

        if(socket_clicked == True): # check if first socket was clicked i.e. output socket
            socket1 = sock[0]
        if(socket1.socket_type == 'in' and socket_clicked == True):
            text = 'Invalid. You can connect only from output socket to input socket.'
            socket_clicked = False
        else:
            text = 'Select upto 5 points on the path of connector or select socket to connect to directly'
            points_list.append(pygame.mouse.get_pos())
            
            if(socket_clicked == False): # check if input destination socket is  clicked
                socket2 = sock[0]
                # create connection between the two sockets
                if(socket2.connected!=True):
                    socket2.connected = True
                    socket1.outgoing.append(socket2) # add to socket's outgoing list
                    socket2.incoming = socket1 # add to socket's incoming list
                    print(sock[0].incoming)
                    #graph[socket1.belongs][socket2.belongs] = 1
                    points_list.append(black)
                    lines.append(points_list)
                    mouse_click_points = []
                    points_list = []
                    socket1 = None
                    socket2 = None
                    print(graph)
                else:
                    text = 'This input socket already has a connection' # change this to just continue after printing error message

            # testing something:
            '''
            if(len(gates_dict) == 3):
                gates_dict[1].outputSocket.val = 1
                print ('+++++++', gates_dict[1].outputSocket.img)
                print(gates_dict[1].outputSocket.outgoing)
                for i in gates_dict[1].outputSocket.outgoing:
                     print(i.belongs)
                     i.val = gates_dict[1].outputSocket.val
                for i in socket_list:
                    print(i.socket_type, i.belongs, i.val)
                print('**********')
            '''
            
    elif(socket_clicked == True):
        print('after socket')
        points_list.append(pygame.mouse.get_pos())
        mouse_click_points.append(pygame.mouse.get_pos()) 
        if(len(mouse_click_points)>5):
                text = 'Pick an output socket within five points'
                points_list = []
                mouse_click_points = []
                socket_clicked = False
        
    elif(button_clicked == True):
        print("clicked elsewhere")
        pos1=pygame.mouse.get_pos()
        #pos=(30,30)
        if(delete_set == True):
            if(len(others)!=0):
                others[0].delete()
                print (graph)
        else:
            put_gate()

    elif(len(others)!=0):
        others[0].change_output()
        print(others[0].val)
        
    print()

buttons_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_gates = pygame.sprite.Group()
socket_list = pygame.sprite.Group()

def put_gate():
             global gates_dict, gate_counter, graph
             print("clicked elaewhree2")
             print(pos1)
             #screen.blit(gate,pos1)
             global clickedgate
             if(clickedgate == 'switch'):
                 g = Switch()
             else:
                 g=Gates(clickedgate)
             global all_sprites
             global text
             text = clickedgate.upper()+" selected. Click on a socket to connect."
             g.rect.x = pos1[0]
             g.rect.y = pos1[1]
             all_sprites.add(g)
             all_gates.add(g)
             g.draw_socket()
             l = all_gates.sprites()
             
             if(len(graph)<len(gates_dict)):
                     graph.append([0]*len(graph))
             for i in range(len(gates_dict)):
                 if(len(graph)!=1):
                     graph[i].append(0)
                 else:
                     graph[0].append(0)

             print(graph)
             print(gates_dict)
             
def main():

    pygame.init()
    pygame.font.init()
    # create all buttons
    and_gate = Button(pygame.image.load("and.png"), pygame.image.load("and1.png"),"and")
    buttons_list.add(and_gate)
    all_sprites.add(and_gate)
    #set coordinates
    and_gate.rect.x = 50
    and_gate.rect.y = 20

    or_gate = Button(pygame.image.load("or.png"), pygame.image.load("or1.png"),"or")
    buttons_list.add(or_gate)
    all_sprites.add(or_gate)
    or_gate.rect.x = 50
    or_gate.rect.y = 80

    not_gate = Button(pygame.image.load("not.png"), pygame.image.load("not1.png"),"not")
    buttons_list.add(not_gate)
    all_sprites.add(not_gate)
    not_gate.rect.x = 50
    not_gate.rect.y = 140
   
    nand_gate = Button(pygame.image.load("nand.png"), pygame.image.load("nand1.png"),"nand")
    buttons_list.add(nand_gate)
    all_sprites.add(nand_gate)
    nand_gate.rect.x = 50
    nand_gate.rect.y = 200

    nor_gate = Button(pygame.image.load("nor.png"), pygame.image.load("nor1.png"),"nor")
    buttons_list.add(nor_gate)
    all_sprites.add(nor_gate)
    nor_gate.rect.x = 50
    nor_gate.rect.y = 260

    xor_gate = Button(pygame.image.load("xor.png"), pygame.image.load("xor1.png"),"xor")
    buttons_list.add(xor_gate)
    all_sprites.add(xor_gate)
    xor_gate.rect.x = 50
    xor_gate.rect.y = 320

    xnor_gate = Button(pygame.image.load("xnor.png"), pygame.image.load("xnor1.png"),"xnor")
    buttons_list.add(xnor_gate)
    all_sprites.add(xnor_gate)
    xnor_gate.rect.x = 50
    xnor_gate.rect.y = 380

    delete_gate = Button(pygame.image.load("DELETE.jpg"), pygame.image.load("deletes.jpg"),"delete")
    buttons_list.add(delete_gate)
    all_sprites.add(delete_gate)
    delete_gate.rect.x = 50
    delete_gate.rect.y = 440

    switch_gate = Button(pygame.image.load("switch0.bmp"), pygame.image.load("switch1.bmp"),"switch")
    buttons_list.add(switch_gate)
    all_sprites.add(switch_gate)
    switch_gate.rect.x = 50
    switch_gate.rect.y = 500

    
    # create user sprite
    user = Button(pygame.image.load("user.jpg"), pygame.image.load("user.jpg"),"user")
    all_sprites.add(user)
    close = False

    global myfont
    myfont = pygame.font.SysFont("Times New Roman",25)
    global label, text
    text = "Welcome to logic gate simulator. Select a gate."
    
    

    # main loop
    while close == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_button(user)
                
        screen.fill((255,255,255))
       
        pygame.draw.line(screen, (0,0,0), (200,0),(200,600))
      
        pos = pygame.mouse.get_pos()
        
        user.rect.x = pos[0]
        user.rect.y = pos[1]

        # try to put this elsewhere
        for i in socket_list:
            if(i.val == 0):
                i.img = pygame.image.load('socket1.jpg')
            elif(i.val == 1):
                i.img = pygame.image.load('socket.jpg')
            i.image = i.img.convert()
            i.image.set_colorkey(white)

       
        
        all_sprites.draw(screen)
        for i in mouse_click_points:
            pygame.draw.circle(screen, red, i,3)
        for i in lines:
            pygame.draw.lines(screen, i[-1], False, i[0:(len(i)-1)])

        label = myfont.render(text, 1, (255,0,0))
        screen.blit(label, (220,10))
        pygame.display.flip()

main()
    
a=pygame.sprite.group()
a.add()
