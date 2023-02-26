import tkinter as tk
from progresspanel import Progresspanel
from time import sleep

root = tk.Tk()

# Use Case 1: Repeat a task independent of iteration number for 5 times
def task_independent():
    print("task1 step")
    sleep(1)
progress_independent = Progresspanel(root, total=5, task=task_independent, title="Task 1 (Independent of iteration)", verbose=True)
progress_independent.pack()

# Use Case 2: Repeat a task dependent on iteration number (self.i) for 5 times
class ProgresspanelDependent(Progresspanel):
    def task(self):
        print("task2 step {}".format(self.i))
        sleep(1)
progress_dependent = ProgresspanelDependent(root, total=5, title="Task 2 (Dependent of iteration)", verbose=True)
progress_dependent.pack()

root.mainloop()
