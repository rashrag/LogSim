import pygame
from pygame import draw
pygame.font.init()

class Form(pygame.Rect,object):
    
    def __init__(self,pos,width,height=None,font=None,fontsize=None,bg=(200,200,200),fgcolor=(0,0,0),curscolor=(0xff0000),hlcolor=(0xa0,0,0),maxlines=0):
        if not font: self.FONT = pygame.font.Font(pygame.font.get_default_font(),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = font
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        
        self.BG = bg
        self.FGCOLOR = fgcolor
        self.CURSCOLOR = curscolor
        self.CURSOR = True
        self.HLCOLOR = hlcolor
        self.MAXLINES = maxlines
        self.TAB = 4
        
        self.OUTPUT = ''
        self.CURSORINDEX = 0
        self.SELECTSTART = 0
        self._x,self._y = pos
        self.SRC = pygame.display.get_surface()
    
    def clear_selection(self):
        if self.SELECTSTART != self.CURSORINDEX:
            select1,select2 = sorted((self.SELECTSTART,self.CURSORINDEX))
            self.OUTPUT = self.OUTPUT[:select1]+self.OUTPUT[select2:]
            self.CURSORINDEX = select1
            return True
        return False
        
    def show(self):
        h = self.FONT.get_height()
        x,y = self._x,self._y
        r = pygame.Rect(x,y,0,h)
        for e,i in enumerate(self.OUTPUT+'\n'):
            if e == self.CURSORINDEX+1: break
            if i not in '\n\t':
                r = pygame.Rect(x,y,*self.FONT.size(i))
                x = r.right
            elif i == '\n':
                r = pygame.Rect(x,y,1,h)
                x = self._x
                y = r.bottom
            else:
                t = self.FONT.size(self.TAB*' ')[0]
                t = ((((x-self._x) / t) + 1) * t ) - (x-self._x)
                r = pygame.Rect(x,y,t,h)
                x = r.right
        
        rclamp = r.clamp(self)
        self._x += rclamp.x - r.x
        self._y += rclamp.y - r.y
        
        clip = self.SRC.get_clip()
        self.SRC.set_clip(self.clip(clip))
        try: self.SRC.fill(self.BG,self)
        except: self.SRC.blit(self.BG,self)
        x = self._x
        y = self._y
        select1,select2 = sorted((self.SELECTSTART,self.CURSORINDEX))
        self.C = []
        for e,i in enumerate(self.OUTPUT):
            if i not in '\n\t':
                self.C.append(pygame.Rect(x,y,*self.FONT.size(i)))
                if select1 <= e < select2:
                    scr.blit(self.FONT.render(i,1,self.HLCOLOR),(x,y))
                else:
                    scr.blit(self.FONT.render(i,1,self.FGCOLOR),(x,y))
                x = self.C[-1].right
            elif i == '\n':
                self.C.append(pygame.Rect(x,y,0,h))
                x=self._x
                y = self.C[-1].bottom
            else:
                t = self.FONT.size(self.TAB*' ')[0]
                t = ((((x-self._x) / t) + 1) * t ) - (x-self._x)
                self.C.append(pygame.Rect(x,y,t,h))
                x = self.C[-1].right
        self.C.append(pygame.Rect(x,y,0,h))
        if self.CURSOR:
            p = self.C[self.CURSORINDEX]
            draw.line(scr,self.CURSCOLOR,p.topleft,(p.left,p.bottom),1)
        pygame.display.update(self)
        self.SRC.set_clip(clip)
            
    def place_cursor(self,pos):
            c = pygame.Rect(pos,(0,0)).collidelist(self.C)
            if c > -1: self.CURSORINDEX = c if pos[0] <= self.C[c].centerx else c + 1
            else:
                l = (pos[1] - self._y) / self.FONT.get_height()
                self.CURSORINDEX = sum([len(i) for i in self.OUTPUT.split('\n')][:l+1])+l
                if self.CURSORINDEX > len(self.OUTPUT): self.CURSORINDEX = len(self.OUTPUT)
                elif self.CURSORINDEX < 0: self.CURSORINDEX = 0
                
    def wakeup(self,ev):
        if ev.type == pygame.KEYDOWN:
            
            if ev.key == pygame.K_RIGHT:
                if self.SELECTSTART != self.CURSORINDEX: self.CURSORINDEX = max((self.SELECTSTART,self.CURSORINDEX))
                elif self.CURSORINDEX < len(self.OUTPUT): self.CURSORINDEX += 1
                
            elif ev.key == pygame.K_LEFT:
                if self.SELECTSTART != self.CURSORINDEX: self.CURSORINDEX = min((self.SELECTSTART,self.CURSORINDEX))
                elif self.CURSORINDEX > 0: self.CURSORINDEX -= 1
                
            elif ev.key == pygame.K_DELETE:
                if not self.clear_selection():
                    self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+self.OUTPUT[self.CURSORINDEX+1:]
            
            elif ev.key == pygame.K_END:
                try:
                    self.CURSORINDEX = self.OUTPUT[self.CURSORINDEX:].index('\n') + self.CURSORINDEX
                except:
                    self.CURSORINDEX = len(self.OUTPUT)
            
            elif ev.key == pygame.K_HOME:
                try:
                    self.CURSORINDEX = self.OUTPUT[:self.CURSORINDEX].rindex('\n') + 1
                except:
                    self.CURSORINDEX = 0
            
            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER:
                self.clear_selection()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+'\n'+self.OUTPUT[self.CURSORINDEX:]
                    self.CURSORINDEX += 1
            
            elif ev.key == pygame.K_BACKSPACE:
                if not self.clear_selection():
                    if self.CURSORINDEX > 0:
                        self.CURSORINDEX -= 1 
                        self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+self.OUTPUT[self.CURSORINDEX+1:]
            
            elif ev.key == pygame.K_UP:
                c = self.C[self.CURSORINDEX]
                self.place_cursor((c.left,c.top-self.FONT.get_height()))

            elif ev.key == pygame.K_DOWN:
                c = self.C[self.CURSORINDEX]
                self.place_cursor((c.left,c.top+self.FONT.get_height()))
                
            elif ev.unicode:
                self.clear_selection()
                self.OUTPUT = self.OUTPUT[:self.CURSORINDEX]+ev.unicode+self.OUTPUT[self.CURSORINDEX:]
                self.CURSORINDEX += 1
            if ev.key not in (K_NUMLOCK,K_CAPSLOCK,K_SCROLLOCK,K_RSHIFT,K_LSHIFT,K_RCTRL,K_LCTRL,K_RALT,K_LALT,K_RMETA,K_LMETA,K_LSUPER,K_RSUPER,K_MODE,K_HELP,K_PRINT,K_SYSREQ,K_BREAK,K_MENU,K_POWER):
                self.SELECTSTART = self.CURSORINDEX
            self.show()
        
        elif (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1) or (ev.type == pygame.MOUSEMOTION and ev.buttons[0]):
            self.place_cursor(ev.pos)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.SELECTSTART = self.CURSORINDEX
            self.show()
    
"""
from pygame import *
from pyca import *

from buttons import *
def clear():
    champ.OUTPUT = ''
    champ.CURSORINDEX=0
    champ.show()
scr = display.set_mode((440,240))
scr.fill(-1)
display.flip()
key.set_repeat(100,25)
champ = Form((20,20),400,height=80,fontsize=20,bgcolor=(190,180,200),maxlines=3)
champ.CURSOR_COLOR = 255,0,0
champ.COLOR = 0,0,0
champ.OUTPUT = 'foobar'
scr.fill((200,200,255),champ)
valid = Button0(' VALID ',(350,105),event.post,(event.Event(QUIT),))
clear = Button0(' CLEAR ',(250,105),clear)
champ.show()
valid.init(),clear.init()
focus(champ)
test = Pyca((champ,valid,clear))
while wait(test).type != QUIT: pass
"""
#if __name__ == "__main__":
from pygame import *
def main():
    scr = display.set_mode((440,180))
    scr.fill(-1)
    scr.blit(font.Font(font.get_default_font(),20).render('your input: ',1,(0,0,0)),(20,20))
    scr.blit(font.Font(font.get_default_font(),20).render('some lines: ',1,(0,0,0)),(20,60))
    scr.blit(font.Font(font.get_default_font(),15).render('hit ESC to quit',1,(0,0,0)),(20,160))
    display.flip()
    key.set_repeat(100,40)
    
    champ = Form((140,20),200,fontsize=20,bg=(200,200,180),hlcolor=(90,40,40),maxlines=1)
    champ.show()
    
    txt = Form((140,60),200,fontsize=17,bg=(200,200,180),hlcolor=(90,40,40),height=80)
    txt.CURSOR = False
    txt.show()
    
    item = champ
    while True:
        ev = event.wait()
        if ev.type == KEYDOWN and ev.key == K_ESCAPE:
            print (champ.OUTPUT)
            print (txt.OUTPUT)
            break
        elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if champ.collidepoint(ev.pos):
                item = champ
                txt.CURSOR = False
                txt.FGCOLOR = 50,50,50
                txt.show()
            elif txt.collidepoint(ev.pos):
                item = txt
                champ.CURSOR = False
                champ.FGCOLOR = 50,50,50
                champ.show()
            item.CURSOR = True
            item.FGCOLOR = 0,0,0
            item.wakeup(ev)
        else:
            item.wakeup(ev)

