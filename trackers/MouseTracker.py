import pyautogui


class MouseTracker:
    def sample(self):
        screen_width, screen_height = pyautogui.size()
        x, y = pyautogui.position()

        rel_x = x / screen_width
        rel_y = y / screen_height

        return rel_x, rel_y
