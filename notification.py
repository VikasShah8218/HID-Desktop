import win32api
import win32con
import win32gui
import threading
import os

class WindowsBalloonTip:
    def __init__(self, title, msg,set_time_out=3):
        icon_path = os.path.join(os.path.dirname(__file__), 'hid.ico')
        message_map = {
            win32con.WM_DESTROY: self.on_destroy,
        }

        # Register the window class.
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wndproc  # Set the window procedure
        wc.lpszClassName = 'PythonTaskbar'
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)

        # Create the window.
        self.hwnd = win32gui.CreateWindow(
            class_atom, 'Taskbar', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
        )
        win32gui.UpdateWindow(self.hwnd)

        # Load the icon for the notification if provided
        if icon_path:
            hicon = win32gui.LoadImage(
                wc.hInstance, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE
            )
        else:
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, title)
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

        # Display the notification
        self.show_balloon(title, msg)

        # Set a timer using threading to destroy the notification after 10 seconds
        threading.Timer(set_time_out, self.destroy).start()
        win32gui.PumpMessages()

    def show_balloon(self, title, msg):
        flags = win32gui.NIF_INFO
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, None, title, msg, 200, 'Python')
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def destroy(self):
        # Destroy the window and notification after the timer ends
        win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    def on_destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.
        return 0  # Return a valid integer to avoid TypeError

    def wndproc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DESTROY:
            return self.on_destroy(hwnd, msg, wparam, lparam)
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

def show_notification(title, message,set_time_out):
    WindowsBalloonTip(title, message,set_time_out=3)

