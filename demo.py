import tkinter as tk
from progresspanel import Progresspanel
from time import sleep

root = tk.Tk()

progresspanel = Progresspanel(root, total=5, title="Task 3 (Dependent of iteration)", verbose=True)
progresspanel.pack()
def task():
    progresspanel.set_total(10)
    for i in range(10):
        progresspanel.update(i)
        print("task3 step {}".format(i))
        sleep(1)
progresspanel.set_task(task)

root.mainloop()
