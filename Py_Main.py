from MainMenu import *

root = MainMenu()
winWidth = "500"
winLength = "350"
root.geometry('{}x{}'.format(winWidth, winLength))
root.title("Main Menu")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()