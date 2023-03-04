import tkinter as tk
from progresspanel import Progresspanel
from time import sleep

root = tk.Tk()
progresspanel = Progresspanel(root, title="Task 1", verbose=True)
progresspanel.pack()


def task():
    total = 10
    progresspanel.set_total(total)
    for i in range(total):
        progresspanel.update(i)
        sleep(1)


progresspanel.set_task(task)

root.mainloop()
