from tkinter import *
a="hello"
def main():
        top = Tk()
        def print_contents(event) :
                print(text.get(1.0, END))
                global a
                a=text.get(1.0, END)
                top.quit()
                

        text = Text(width="20", height="10")

        text.insert(END, "hello, ")
        text.insert(END, "world")
        text.pack()


        button1 = Button(top, text='Disp')
        button1.bind('<Button-1>', print_contents)
        button1.pack()



        mainloop()
