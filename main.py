from tkinter import *

vnpr_root = Tk()
# widthxheight
 
vnpr_root.geometry("1214x770")
vnpr_root.title("Vehicle Number Plate Recognition System")
photo = PhotoImage(file="Frame6.png")

# mansi = Label(text="Vehicle Number Plate Recognition System")
# mansi.pack()
img_label = Label(image=photo)
img_label.pack()



vnpr_root.mainloop()


