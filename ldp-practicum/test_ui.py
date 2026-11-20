import time
import unittest
from app import App

class UITests(unittest.TestCase):
    def test_step_scale_stop_and_full_run(self):
        app=App();app.withdraw()
        try:
            app.update();app.integer.set(True);app.start(False)
            end=time.monotonic()+3
            while not app.events and time.monotonic()<end:app.update();time.sleep(.01)
            self.assertTrue(app.events);self.assertTrue(app.running)
            before=[[v.get() for v in row] for row in app.cells]
            app.scale.set(150);app.update();self.assertEqual(before,[[v.get() for v in row] for row in app.cells])
            app.stop();app.update();self.assertFalse(app.running)
            app.start(True);end=time.monotonic()+8
            while app.running and time.monotonic()<end:app.update();time.sleep(.01)
            self.assertFalse(app.running);self.assertEqual(app.events[-1].status,'optimal');self.assertEqual(app.events[-1].objective,67)
            self.assertIn('67',app.result.get('1.0','end'))
        finally:app.stop();app.destroy()

if __name__=='__main__':unittest.main()
