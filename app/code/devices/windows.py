import ctypes
import time
import win32gui
import win32con
import pygetwindow as gw  # Assuming you have pygetwindow installed

from ..media.cropping import crop_team_names
from ..media.preprocess_image import preprocess_image_adding_rectangles
from ..media.image_to_text import get_team_names
from .move_mouse import move_mouse_to_game, click_back_button, slide_next_player, point_last_player, drag_to_team_stats, \
    drag_to_next_stats
from .screenshots import take_team_screenshot
from ..devices.screenshots import get_team_stats_photo, take_screenshot


def get_window_rect(hwnd):
    # Get the window's rectangle coordinates
    rect = win32gui.GetWindowRect(hwnd)
    return rect


def bring_window_to_front(hwnd):
    # Restore and bring the window to the front
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Bring the window to the foreground
    ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 is SW_SHOW
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    ctypes.windll.user32.SetFocus(hwnd)

    # Allow time for the window to come to the foreground
    time.sleep(1)


def screenshot_window_by_title(window_title, n_games, folder_path, tesseract_path):
    # Get the window handle for the specified title
    hwnds = gw.getWindowsWithTitle(window_title)
    if hwnds:
        hwnd = hwnds[0]._hWnd  # Get the window handle

        # Get the window's coordinates and size
        rect = get_window_rect(hwnd)
        left, top, right, bottom = rect

        # Ensure the window is brought to the front
        bring_window_to_front(hwnd)

        game = 0
        # Move the mouse to the top-left corner of the window
        for game in range(0, min(5, n_games)):
            print(f"Game {game}")
            move_mouse_to_game(game, left, top, right, bottom)

            teams_path = take_team_screenshot(bottom, left, right, top, folder_path)
            print("Teams path: ", teams_path)
            out_path = f'{folder_path}/Stats Cropped/Team Names-{game}.png'
            crop_team_names(teams_path, out_path)
            team_names = get_team_names(out_path, tesseract_path)
            team_names_out = team_names[0] + "-" + team_names[1]
            drag_to_team_stats(bottom, left, right, top)

            for i in range(0, 1): #TODO increase to get all stats
                path = get_team_stats_photo(bottom, left, right, top, folder_path, team_names_out, i)
                time.sleep(1)
                # TODO function to obtain the stats of players
                preprocess_image_adding_rectangles(path)
                exit(3)



            # Go back to the team window
            click_back_button(bottom, left, right, top)


        while game < n_games:
            print(f"Player {game}")
            slide_next_player(bottom, left, right, top)
            move_mouse_to_game(5, left, top, right, bottom)
            take_screenshot(bottom, left, right, top, folder_path)
            time.sleep(2)
            # Go back to the team window
            click_back_button(bottom, left, right, top)
            game+=1

        point_last_player(bottom, left, right, top)


    else:
            print(f"Window with title '{window_title}' not found.")

