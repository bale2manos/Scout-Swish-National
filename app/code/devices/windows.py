import ctypes
import time
import win32gui
import win32con
import pygetwindow as gw  # Assuming you have pygetwindow installed
import os

from utils.validator import filter_first_stats, check_players_names
from ..media.cropping import crop_team_names
from ..media.preprocess_image import preprocess_image_adding_rectangles
from ..media.image_to_text import get_team_names, get_players_names, get_team_stats, get_players_numbers
from .move_mouse import move_mouse_to_game, click_back_button, drag_to_team_stats, \
    move_mouse_to_next_team_stats, drag_to_next_game
from .screenshots import take_team_screenshot
from ..devices.screenshots import get_team_stats_photo
from ..data.excel import save_to_excel
from ..utils.utils import remove_temp_images


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

        # Move the mouse to the top-left corner of the window
        for game in range(0, min(2, n_games)):
            game_stats, local_away, team, team_names = analyze_game(bottom, folder_path, game, left, right,
                                                                    tesseract_path, top)
            excel_name = f"{folder_path}/Results/{team_names[0]} vs {team_names[1]}.xlsx"
            save_to_excel(game_stats, excel_name)

            # Go back to the team window
            click_back_button(bottom, left, right, top)

            # Rename the folder in f'{folder_path}/Stats Cropped/{game}/ to the name of the game
            if not os.path.exists(f'{folder_path}/Stats Cropped/{team_names[0]} vs {team_names[1]}'):
                os.rename(f'{folder_path}/Stats Cropped/{game}',
                          f'{folder_path}/Stats Cropped/{team_names[0]} vs {team_names[1]}')

        game = 2
        while game < n_games:
            # Drag to the next game
            drag_to_next_game(bottom, left, right, top)
            game_stats, local_away, team, team_names = analyze_game(bottom, folder_path, game, left, right,
                                                                    tesseract_path, top)


            excel_name = f"{folder_path}/Results/{team_names[0]} vs {team_names[1]}.xlsx"
            save_to_excel(game_stats, excel_name)

            # Go back to the team window
            click_back_button(bottom, left, right, top)

            # Rename the folder in f'{folder_path}/Stats Cropped/{game}/ to the name of the game
            if not os.path.exists(f'{folder_path}/Stats Cropped/{team_names[0]} vs {team_names[1]}'):
                os.rename(f'{folder_path}/Stats Cropped/{game}', f'{folder_path}/Stats Cropped/{team_names[0]} vs {team_names[1]}')

            game += 1


    else:
        print(f"Window with title '{window_title}' not found.")


def analyze_game(bottom, folder_path, game, left, right, tesseract_path, top):
    print(f"Game {game}")
    move_mouse_to_game(game, left, top, right, bottom)
    # Create the folder for the game
    if not os.path.exists(f'{folder_path}/Stats Cropped/{game}'):
        os.makedirs(f'{folder_path}/Stats Cropped/{game}')
    # Get the team names
    teams_path = take_team_screenshot(bottom, left, right, top, folder_path)
    print("Teams path: ", teams_path)
    out_path = f'{folder_path}/Stats Cropped/{game}/Team Names.png'
    crop_team_names(teams_path, out_path)
    team_names = get_team_names(out_path, tesseract_path)
    # Get stats for each team
    drag_to_team_stats(bottom, left, right, top)
    game_stats = {}
    local_away = 0
    for team in team_names:
        game_stats[team] = {}
        path = get_team_stats_photo(bottom, left, right, top, folder_path, team, 0, game)
        time.sleep(1)

        preprocess_path = preprocess_image_adding_rectangles(path)

        player_numbers = get_players_numbers(preprocess_path, tesseract_path, local_away)

        players_names = get_players_names(preprocess_path, tesseract_path)

        # Add the player numbers to the player names
        print("Player numbers: ", player_numbers)
        print("Players names: ", players_names)
        print("Length of player numbers: ", len(player_numbers))
        print("Length of players names: ", len(players_names))
        if len(players_names) > len(player_numbers):
            print("Error: The number of players names is less than the number of player numbers")
            players_names = check_players_names(players_names)
            print("Longitud de la lista despues de check: ", len(players_names))

        if len(players_names) == len(player_numbers):
            for i in range(len(players_names)):
                players_names[i] = player_numbers[i] + ". " + players_names[i]

        # Add players names to the dictionary
        for player in players_names:
            game_stats[team][player] = {}

        # Get the stats of the team
        stats = get_team_stats(preprocess_path, tesseract_path)
        stats = filter_first_stats(stats)


        # Add stats to the dictionary, first player corresponds to the first element of stats
        j = 0
        print("Game stats:", game_stats)
        print("Stats: ", stats)
        print("Length of stats: ", len(stats))
        print("Length of players names: ", len(players_names))
        for player in players_names:
            game_stats[team][player] = stats[j]
            j += 1

        print("Game stats:", game_stats)

        # TODO get more stats of the same team

        # Go to the next team stats
        local_away = 1
        move_mouse_to_next_team_stats(bottom, left, right, top)
    return game_stats, local_away, team, team_names


