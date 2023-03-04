import tkinter as tk
from progresspanel import Progresspanel
from time import sleep

root = tk.Tk()
progresspanel = Progresspanel(root, title="Task 1", verbose=True)
progresspanel.pack()


def task():
    progresspanel.set_total(10)
    for i in range(10):
        progresspanel.update(i)
        sleep(1)


progresspanel.set_task(task)

root.mainloop()
