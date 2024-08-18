import time

import pyautogui


def get_team_stats_photo(bottom, left, right, top, folder_path, team_name, num_stats, n_game):
    # Take a screenshot of the region corresponding to the window
    time.sleep(2)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    file_path = f"{folder_path}/Stats Cropped/{n_game}/{team_name}-{num_stats}.png"
    screenshot.save(file_path)

    return file_path


def take_screenshot(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(0.5)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"{folder_path}/Screenshot_{timestamp}.png"
    screenshot.save(file_path)

def take_team_screenshot(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(2)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"{folder_path}/Teams-{timestamp}.png"
    screenshot.save(file_path)
    time.sleep(2)
    return file_path
