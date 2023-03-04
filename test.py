import unittest
from tkinter import Tk
from progresspanel import Progresspanel, Status


class TestProgressPanel(unittest.TestCase):
    
    def setUp(self):
        self.parent = Tk()
        self.total = 10
        self.progress_panel = Progresspanel(self.parent, self.total)
        
    def tearDown(self):
        self.parent.destroy()
        
    def test_set_total(self):
        new_total = 5
        self.progress_panel.set_total(new_total)
        self.assertEqual(self.progress_panel.total, new_total)
        
    def test_set_task(self):
        def new_task():
            pass
        
        self.progress_panel.set_task(new_task)
        self.assertEqual(self.progress_panel.task, new_task)
        
    def test_update(self):
        i = 3
        self.progress_panel.update(i)
        self.assertEqual(self.progress_panel.i, i)
        
    def test_is_pausing_or_terminating(self):
        self.progress_panel.status = Status.PAUSING
        self.assertTrue(self.progress_panel.is_pausing_or_terminating())
        
        self.progress_panel.status = Status.TERMINATING
        self.assertTrue(self.progress_panel.is_pausing_or_terminating())
        
        self.progress_panel.status = Status.RUNNING
        self.assertFalse(self.progress_panel.is_pausing_or_terminating())
        
    def test_is_pause_resumed(self):
        self.assertFalse(self.progress_panel.is_pause_resumed())
        
        self.progress_panel._pause_resumed = True
        self.assertTrue(self.progress_panel.is_pause_resumed())

unittest.main()
