from threading import Thread
from time import time
from tkinter import ttk
from datetime import timedelta


class Status:
    """
    Status of the task. Notice, PAUSING and TERMINATING are not final states.
    PAUSING means that the user has clicked the pause button, and the task will
    be paused after the current iteration is done and goes into PAUSED state
    afterwards. Same for TERMINATING and TERMINATED.
    """
    RUNNING = 1
    PAUSING = 2
    PAUSED = 3
    TERMINATING = 4
    TERMINATED = 5


class Progresspanel(ttk.Frame):
    """
    Task is a module that runs a loop in an indivisual thread that does something,
    and can be paused, resumed, and terminated. It has buttons and progress_bar
    pre-set in self.frame for easy use.
    """

    def __init__(self, parent, total: int = 1, task: callable = None, title: str = None, verbose: bool = True):
        """
        :param parent: parent widget
        :param total: total number of iterations for self.i in task_loop to iterate.
            User can set this in set_iteration_num().
        :param task: user-defined task to be run in a loop. This should be customized.
            User can set this in set_task() or overwrite task().
        :param title: title of the task. It will be shown in the progress panel.
        :param verbose: whether to print out the status of the task to terminal in pre-defined
            after_ methods. User can also use it in overwritten after_ methods for debugging.
        :param i: current iteration number
        :param status: status of the task. It can be one of the following:
            Status.RUNNING, Status.PAUSING, Status.PAUSED, Status.TERMINATING, Status.TERMINATED
        :param _time_per_iteration: time per iteration in seconds to estimate the remaining time.
        """
        super().__init__(parent)
        self.i = 0
        self.status = Status.TERMINATED
        self.parent = parent
        self.set_total(total)
        self.set_task(task)
        self.title = title
        self.set_verbose(verbose)
        self._time_per_iteration = 0
        self._create_widgets()

    def set_total(self, total):
        """
        Set the total number of iterations for self.i in task_loop to iterate.
        """
        if total <= 0:
            raise ValueError("Iteration number must be larger than 0.")
        self.total = total

    def set_task(self, task: callable):
        """
        Set the task callback function.
        """
        if task is None:
            self.task = self.task
        else:
            self.task = task

    def set_verbose(self, verbose: bool):
        """
        Set verbose mode.
        """
        self.verbose = verbose

    def task(self):
        """
        User-defined individual task to be run in a loop. This should be customized
        and overwritten by users. Make sure to use self.i as the loop counter.
        """
        pass

    def is_pausing_or_terminating(self):
        """
        Check if the task is in PAUSING or TERMINATING state. This is useful for
        user to stop promptly before running other time-consuming operations in
        user-defined task() after user clicks pause or terminate button.
        """
        if self.status == Status.PAUSING or self.status == Status.TERMINATING:
            return True
        else:
            return False

    def after_started(self):
        """
        Placeholder for user-defined function to be run when the task is started.
        """
        if self.verbose:
            print("Started!")

    def after_resumed(self):
        """
        Placeholder for user-defined function to be run when the task is resumed.
        """
        if self.verbose:
            print("Resumed!")

    def after_paused(self):
        """
        Placeholder for user-defined function to be run when the task is paused.
        """
        if self.verbose:
            print("Paused!")

    def after_terminated(self):
        """
        Placeholder for user-defined function to be run when the task is terminated
        by user.
        """
        if self.verbose:
            print("Terminated!")

    def after_completed(self):
        """
        Placeholder for user-defined function to be run when the task is normally 
        completed (automatically terminated after all interations are done).
        """
        if self.verbose:
            print("Done!")

    def _create_widgets(self):
        """
        Create widgets for progress panel, including buttons and progress bar.
        """
        frame_upper = ttk.Frame(self)
        frame_upper.pack()
        if self.title is not None:
            ttk.Label(frame_upper, text=self.title).pack(side="top")
        self._progress_bar = ttk.Progressbar(
            frame_upper, orient="horizontal", length=200, mode="determinate")
        self._progress_bar.pack(side="left")
        frame_middle = ttk.Frame(self)
        frame_middle.pack()
        self._label_status = ttk.Label(
            frame_middle, text=self._get_progress_notice())
        self._label_status.pack(side="left")
        frame_lower = ttk.Frame(self)
        frame_lower.pack()
        self._button_start = ttk.Button(
            frame_lower, text="Start", command=self._start)
        self._button_start.pack(side="left")
        self._button_pause = ttk.Button(
            frame_lower, text="Pause", command=self._pause)
        self._button_pause["state"] = "disabled"
        self._button_pause.pack(side="left")
        self._button_terminate = ttk.Button(
            frame_lower, text="Terminate", command=self._terminate)
        self._button_terminate["state"] = "disabled"
        self._button_terminate.pack(side="left")

    def _get_progress_notice(self):
        """
        Get the remaining time.
        """
        remaining_time = int(self._time_per_iteration * (self.total - self.i))
        if self.status == Status.TERMINATED:
            return "Ready"
        return "Running: {}/{}. Time left: {}".format(self.i + 1, self.total, timedelta(seconds=remaining_time) if remaining_time > 0 else "--:--:--")

    def _start(self):
        """
        Start the task loop in a thread.
        """
        if self.status != Status.RUNNING:
            if self.status != Status.PAUSED:
                self._label_status.config(text=self._get_progress_notice())
                self.after_started()
            else:
                self.after_resumed()
            self.status = Status.RUNNING
            self._progress_bar["value"] = self.i / self.total * 100
            self._button_start["state"] = "disabled"
            self._button_pause["state"] = "normal"
            self._button_terminate["state"] = "normal"
            thread = Thread(target=self._task_loop)
            thread.setDaemon(True)
            thread.start()

    def _task_loop(self):
        """
        Loop that runs the user-customized task defined in task method.
        """
        try:
            while self.status == Status.RUNNING and self.i < self.total:
                time_start = time()
                self._label_status.config(text=self._get_progress_notice())
                self.task()
                time_end = time()
                if self.is_pausing_or_terminating():
                    break
                self._time_per_iteration = (
                    self._time_per_iteration * self.i + time_end - time_start) / (self.i + 1)
                self.i += 1
                self._progress_bar["value"] = self.i / self.total * 100
            if self.status == Status.RUNNING:
                self._reset()
                self._label_status.config(text="Done!")
                self.after_completed()
            elif self.status == Status.TERMINATING:
                self._reset()
                self.after_terminated()
            elif self.status == Status.PAUSING:
                self._button_start["state"] = "normal"
                self.status = Status.PAUSED
                self.after_paused()
                if self.i == self.total:
                    self._reset()
                    self._label_status.config(text="Done!")
        except Exception as e:
            self._pause()
            self._label_status.config(text="Error: {}".format(e))
            self._button_start["state"] = "normal"
            self.status = Status.PAUSED
            self.after_paused()
            raise e

    def _reset(self):
        """
        Reset the task to the initial state.
        """
        self.status = Status.TERMINATED
        self.i = 0
        self._time_per_iteration = 0
        self._button_terminate["state"] = "disabled"
        self._button_pause["state"] = "disabled"
        self._button_start["state"] = "normal"
        self._button_start.config(text="Start")
        self._progress_bar["value"] = 0
        self._label_status.config(text=self._get_progress_notice())

    def _pause(self):
        """
        Pause the task.
        """
        self.status = Status.PAUSING
        self._button_pause["state"] = "disabled"
        self._button_start.config(text="Resume")

    def _terminate(self):
        """
        Terminate the task.
        """
        if self.status == Status.PAUSED:
            self.after_terminated()
            self._reset()
        self.status = Status.TERMINATING
        self._button_pause["state"] = "disabled"
        self._button_terminate["state"] = "disabled"
