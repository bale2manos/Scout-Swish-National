import time

import pyautogui


def move_mouse_to_game(n, left, top, right, bottom):
    player_offset = n * (bottom - top) // 9 #TODO find offset

    # Move the mouse to the middle of the window
    pyautogui.moveTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset)
    time.sleep(2)

    # Click the mouse
    pyautogui.click()
    time.sleep(2)

    move_to_game_stats(bottom, left, right, top)



def move_to_game_stats(bottom, left, right, top):
    # Now go to the 2/3 of the windows width and at 1/6 of the height
    pyautogui.moveTo(left + 2 * (right - left) // 3, top + (bottom - top) // 8)
    time.sleep(2)
    # Click the mouse
    pyautogui.click()
    time.sleep(2)


def point_last_player(bottom, left, right, top):
    player_offset = 4 * (bottom - top) // 9
    pyautogui.moveTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset)


def click_back_button(bottom, left, right, top):
    # Move the mouse to the top-left corner of the window, 1/10 of the width and 1/10 of the height
    pyautogui.moveTo(left + (right - left) // 14, top + (bottom - top) // 12)
    time.sleep(1)
    # Click the mouse
    pyautogui.click()
    time.sleep(2)


def slide_next_player(bottom, left, right, top):
    # Move the mouse to the last player
    print("Moving to the next player")
    player_offset = 4 * (bottom - top) // 9
    point_last_player(bottom, left, right, top)
    time.sleep(1)

    # Slide up 2/15 of the height, in the same x position
    pyautogui.dragTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset - 5* (bottom - top) // 39, 1, button='left')
    time.sleep(2)

def drag_to_team_stats(bottom, left, right, top):
    # Move the mouse to the middle of the window
    pyautogui.moveTo(left + (right - left) // 2, top + (bottom - top) // 2)
    time.sleep(2)

    # Drag the mouse to the 10% of the window height, in the same x position
    pyautogui.dragTo(left + (right - left) // 2, top + (bottom - top) // 10, 1, button='left')
    time.sleep(2)

def drag_to_next_stats(bottom, left, right, top):
    # Move the mouse to the middle of the window
    pyautogui.moveTo(left + (right - left) // 2, top + (bottom - top) // 2)
    time.sleep(2)

    # Drag the mouse to the left extreme, in the same y position
    pyautogui.dragTo(left, top + (bottom - top) // 2, 1, button='left')
