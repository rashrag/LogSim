import pygame,text
#import inputbox
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
screen = pygame.display.set_mode([800,600])
img="dummy.jpg"
d={'and':'and.png',"":'dummy.png','or':'or.png','nor':'nor.png','not':'not.png','nand':'nand.png','xor':'xor.png','save':'save.png','xnor':'xnor.jpg'}
#class to create gates
class Gates(pygame.sprite.Sprite):
    def __init__(self,gate):
         pygame.sprite.Sprite.__init__(self)
         self.gatetype=gate
         global d
         img = pygame.image.load(d[gate])
         self.image = img.convert()
         self.image.set_colorkey(white)
        # Fetch the rectangle with the dimensions of the image. Set position by using rect.x, rect.y
        # Coordinates to put the button at and accessing those coordinates knowing the size will also be easy.
         self.rect = self.image.get_rect()
clickedgate=""
count=0
touch=0
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
        global count
        self.c=count
        touch=count
        count+=1
        global touch
     
    def change_colour(self, flag):
        x = self.rect.x
        y = self.rect.y
        global clickedgate
        print(clickedgate)
        if(flag == False):
            self.image = self.change.convert()
            clickedgate=self.gatename
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = self.original.convert()
            clickedgate = ""
            self.image.set_colorkey(white)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    
#......................................................................................................................................................................
#.........................................................................................................................................................................


            
event=pygame.event.poll()
pos1=(30,30)
hit=[1]
hit1=[1]

def check_button(user):
    global pos1
    global hit,hit1
    hit = pygame.sprite.spritecollide(user, buttons_list, False)
    print(hit)
    if(len(hit)!=0):#and hit1 is hit):
        hit[0].change_colour(hit[0].clicked)
        #hit[0].put_button()
        hit1=hit
        #print("hope name:",hit[0].name)
        print()
        print(hit[0].clicked)
        hit[0].clicked = not(hit[0].clicked)
        print(hit[0].clicked)
        global touch
        touch= not(touch)
    elif(len(hit)==0):
        print("clicked elsewhere")
        pos1=pygame.mouse.get_pos()
        #pos=(30,30)
        put_gate()
buttons_list = pygame.sprite.Group()
save_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_gates = pygame.sprite.Group()
def put_gate():
             print("clicked elaewhree2")
             print(pos1)
             #screen.blit(gate,pos1)
             global clickedgate
             g=Gates(clickedgate)
             global all_sprites
             g.rect.x = pos1[0]
             g.rect.y = pos1[1]
             all_sprites.add(g)
             all_gates.add(g)
             l = all_gates.sprites()
             print(l[0].gatetype)
             #len(all_sprites)-1=pos
             global screen
             
def main():

    pygame.init()

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
    #or_gate.setText('OR')

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

    save_gate = Button(pygame.image.load("save.png"), pygame.image.load("save.png"),"save")
    save_list.add(save_gate)
    all_sprites.add(save_gate)
    save_gate.rect.x = 50
    save_gate.rect.y = 500
    
    # create user sprite
    user = Button(pygame.image.load("user.jpg"), pygame.image.load("user.jpg"),"user")
    all_sprites.add(user)
    close = False

    
    global hit
    # main loop
    while close == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            elif (event.type == pygame.MOUSEBUTTONDOWN):# and len(hit)==1):
                    if(pygame.sprite.spritecollide(user, save_list, False)):
                        print("clicked save")
                        #surf = pygame.display.set_mode((320,240))
                        #display_box(surf,"")
                        #print (ask(surf, "Name") + " was entered")
                        #inp = int(inputbox.ask(screen, 'Message'))
                        text.main()
                        b=text.a
                        print("name:",b,type(b))
                        #b=b+".jpg"
                        pygame.image.save(screen,'h.jpg')#str(b))
                        print('img saved')
                    else:
                        check_button(user)
                
        screen.fill((255,255,255))
       
        pygame.draw.line(screen, (0,0,0), (200,0),(200,600))
      
        pos = pygame.mouse.get_pos()
        #screen.(gate,pos1)
        
        user.rect.x = pos[0]
        user.rect.y = pos[1]
        all_sprites.draw(screen)
        pygame.display.flip()

main()
    
a=pygame.sprite.group()
a.add()
