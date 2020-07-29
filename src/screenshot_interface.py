from abc import ABC, abstractmethod


class PlatformScreenshot(ABC):

    @abstractmethod
    def get_windows_and_monitors_names(self):
        pass

    @abstractmethod
    def select_window(self, window_name):
        pass

    @abstractmethod
    def screenshot_all_window(self):
        pass

    @abstractmethod
    def screenshot(self, x, y, width, height):
        pass
