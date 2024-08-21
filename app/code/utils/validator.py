import os
import re


def check_over_50_over_under(lines):
    if len(lines) > 7 and float(lines[7]) > 50:
        # If number is over 100, add a decimal point after the second character, if  not add it after the first character
        if float(lines[7]) > 100:
            lines[7] = lines[7][:2] + '.' + lines[7][2:]
        else:
            lines[7] = lines[7][:1] + '.' + lines[7][1:]


def check_over_40_points(lines):
    if len(lines) > 2 and float(lines[2]) > 40:
        # Add a decimal point after the first character
        lines[2] = lines[2][:1] + '.' + lines[2][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 2 and len(lines[2]) > 1 and lines[2][0] == '0' and lines[2][1] != '.':
        lines[2] = lines[2][:1] + '.' + lines[2][1:]


def check_over_5_PF(lines):
    if len(lines) > 6 and float(lines[6]) > 5:
        # Add a decimal point after the first character
        lines[6] = lines[6][:1] + '.' + lines[6][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 6 and len(lines[6]) > 1 and lines[6][0] == '0' and lines[6][1] != '.':
        lines[6] = lines[6][:1] + '.' + lines[6][1:]


def check_over_20_3P(lines):
    if len(lines) > 5 and float(lines[5]) > 20:
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 > float(lines[2]):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 == float(lines[2]) and (float(lines[4]) != 0 or float(lines[3]) != 0):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[5]) > 1 and lines[5][0] == '0' and lines[5][1] != '.':
        lines[5] = lines[5][:1] + '.' + lines[5][1:]


def check_over_20_2FG(lines):
    if len(lines) > 4 and float(lines[4]) > 20:
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 > float(lines[2]):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 == float(lines[2]) and (float(lines[3]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[4]) > 1 and lines[4][0] == '0' and lines[4][1] != '.':
        lines[4] = lines[4][:1] + '.' + lines[4][1:]


def check_over_30_FT(lines):
    if len(lines) > 3 and float(lines[3]) > 30:
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
    elif len(lines) > 3 and float(lines[3]) > float(lines[2]):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are over the total points")
    elif len(lines) > 3 and float(lines[3]) == float(lines[2]) and (float(lines[4]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are equal to the total points")

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[3]) > 1 and lines[3][0] == '0' and lines[3][1] != '.':
        lines[3] = lines[3][:1] + '.' + lines[3][1:]


def check_minutes(lines):
    if len(lines) > 1 and ':' not in lines[1]:
        # After the first two chars, add the colon
        lines[1] = lines[1][:2] + ':' + lines[1][2:]
        # After the fifth char, add the following numbers to the next line
        lines.insert(2, lines[1][5:])
        # Remove the numbers from the first line
        lines[1] = lines[1][:5]

    print("Lines after minutes check: ", lines)


def double_check_points(lines):
    if len(lines) > 5:
        free_throws_pts = float(lines[3]) * 1
        two_points_pts = float(lines[4]) * 2
        three_points_pts = float(lines[5]) * 3
        total_points = float(lines[2])
        # I want to check if the points match but give a certain amount of possible error, up to 1 point
        if abs(free_throws_pts + two_points_pts + three_points_pts - total_points) > 1:
            print("Points don't match")
            print(f"Free throws: {free_throws_pts}, 2 points: {two_points_pts}, 3 points: {three_points_pts}, total: {total_points}")
            # Add a decimal point after the first character
            lines[2] = lines[2][:1] + '.' + lines[2][1:]


def check_data(lines):
    check_minutes(lines)
    check_over_40_points(lines)
    check_over_30_FT(lines)
    check_over_20_2FG(lines)
    check_over_20_3P(lines)
    check_over_5_PF(lines)
    check_over_50_over_under(lines)
    double_check_points(lines)


def filter_first_stats(stats):
    # Remove from every player the fourth element
    for stat in stats:
        try:
            if len(stat) < 5:
                if len(stat[0]) != 5:
                    # Insert the characters after XX:XX to the next element
                    if ':' not in stat[0] and len(stat[0]) >= 4:
                        print("Stat error: ", stat[0])
                        stat.insert(1, stat[0][4:])
                        # Add a : after the second character
                        stat[0] = stat[0][:2] + ':' + stat[0][2:4]
                        print("Stat fixed: ", stat)
                    elif len(stat[0]) > 5:
                        print("Stat error: ", stat[0])
                        stat.insert(1, stat[0][5:])
                        stat[0] = stat[0][:5]
                        print("Stat fixed: ", stat)
                    else:
                        print("Stat error can't fix: ", stat[0])
                        raise ValueError("Minutes error")
                if len(stat[1]) > 2:                         # Can't score more than 99 points
                    print("Stat error: ", stat[1])
                    if check_points(stat) is None:
                        # Get last two characters and remove the rest
                        if '/' not in stat[1][-2:] and '%' not in stat[1][-2:] and '-' not in stat[1][-2:]:
                            stat[1] = stat[1][-2:]
                            print("Stat fixed: ", stat)
                        else:
                            print("Stat error can't fix: ", stat[1])
                            raise ValueError("Points error")

                    print("Points fixed: ", stat)
                if not is_valid_scored_attempted(stat[2]):
                    # Check if 100% is inside the string.
                    print("Free throws has an error: ", stat[2])
                    if '100%' in stat[2]:
                        index = stat[2].index('100%')
                        stat.insert(3, '100%')
                        if len(stat[2][index + 4:]) > 0:
                            stat.insert(4, stat[2][index + 4:])
                        stat[2] = stat[2][:index]
                        print("Stat fixed: ", stat[2])
                    elif '%' in stat[2] and stat[2][stat[2].index('%') - 3] == '/':
                        index = stat[2].index('%')
                        stat.insert(3, stat[2][index - 1:])
                        if len(stat[2][:index - 1]) > 0:
                            stat.insert(4, stat[2][:index - 1])
                        stat[2] = stat[2][:index-1]
                        print("Stat fixed: ", stat)
                    elif '%' in stat[2]:
                        index = stat[2].index('%')
                        stat.insert(3, stat[2][index - 2:])
                        if len(stat[2][:index - 2]) > 0:
                            stat.insert(4, stat[2][:index - 2])
                        stat[2] = stat[2][:index]
                        print("Stat fixed: ", stat[2])
                    else:
                        print("Free throws unsolved error: ", stat[2])
                        raise ValueError("Free throws are wrong")
                if not is_valid_percentage(stat[3]) and stat[3]!="0%":
                    print("Free throws % has an error: ", stat[3])
                    if '%' in stat[3]:
                        index = stat[3].index('%')
                        stat.insert(4, stat[3][index + 1:])
                        stat[3] = stat[3][:index + 1]
                        print("Stat fixed: ", stat[3])
                    else:
                        print("Free throws % unsolved error: ", stat[3])
                        raise ValueError("Free throws % are wrong")
                if not is_valid_scored_attempted(stat[4]):
                    print("2FG has an unsolved error: ", stat[4])
                    raise ValueError("2FG are wrong")
        except Exception as e:
            print("Error filtering stats: ", e)
            # If length of stat is less than 5, update it to 5
            while len(stat) < 5:
                stat.append('-')
            print("Stat length fixed: ", stat)
            # Continue to the next stat
            
            print("Stat fixed: ", stat)
            continue

    for i in range(len(stats)):
        print("Stat pre pop: ", stats[i])
        stats[i].pop(3)
        print("Stat post pop: ", stats[i])
        # If length of stat is bigger than 4, cut it to 4
        if len(stats[i]) > 4:
            stats[i] = stats[i][:4]
            print("Stat cut: ", stats[i])

        print("Stat before filtering: ", stats[i])
        if len(stats[i][0]) != 5 or ':' not in stats[i][0]:
            stats[i][0] = '-'

        print("Stat after minutes filtering: ", stats[i])
        if type(stats[i][1]) == str:
            if len(stats[i][1]) > 2 or '/' in stats[i][1] or '%' in stats[i][1] or '-' in stats[i][1]:
                stats[i][1] = '-'
        elif float(stats[i][1]) > 50:
            # Divide the number by 10
            stats[i][1] = str(float(stats[i][1]) / 10)


        print("Stat after points filtering: ", stats[i])
        if len(stats[i][2]) > 5 or len(stats[i][2]) < 3 or '/' not in stats[i][2] or '%' in stats[i][2]:
            stats[i][2] = '-'

        print("Stat after 2FG filtering: ", stats[i])
        if len(stats[i][3]) > 5 or len(stats[i][3]) < 3 or '/' not in stats[i][3] or '%' in stats[i][3] or '-' in stats[i][3]:
            stats[i][3] = '-'

    print("\nStats after filtering: ", stats, "\n")

    return stats



def is_valid_scored_attempted(field_goal: str) -> bool:
    # IMPORTANT: Checks up to 30 shots, if you need more, change the pattern
    pattern = r'^(?:[0-9]|[1-4][0-9]|40)\/(?:[0-9]|[1-4][0-9]|40)$'
    if re.match(pattern, field_goal):
        scored, attempted = map(int, field_goal.split('/'))
        return scored <= attempted

    return False



def is_valid_percentage(percentage: str) -> bool:
    # IMPORTANT: Checks up to 100% and 1-100% (no decimals)
    pattern = r'^([1-9][0-9]?|100)%$'
    return bool(re.match(pattern, percentage))


def check_points(stat) :
    """
    Parse a stat string in the format "2211/1479%" and assigns values to stat array.

    :param stat: List with stat values.
    :return: Dictionary with stat values or None if invalid input.
    """
    # Regular expression to match the format "2211/1479%"
    stat_string = stat[1]
    pattern = r'^(\d{1,2})(\d{1,2})/(\d{1,2})(\d{1,2})%$'
    match = re.match(pattern, stat_string)

    if not match:
        print("Invalid format")
        return None

    # Extract components
    stat1 = int(match.group(1))
    scored = int(match.group(2))
    attempted = int(match.group(3))
    stat3 = int(match.group(4))

    # Validate components
    if scored > attempted:
        print("Invalid stats: scored is greater than attempted")
        return None

    if scored > 30 or attempted > 30:
        print("Invalid stats: scored or attempted is greater than 30")
        return None

    # Assign values to the stat dictionary
    stat[1] = stat1
    stat.insert(2, f"{scored}/{attempted}")
    stat.insert(3, f"{stat3}%")
    return stat

def check_players_names(players_names):
    current_path = os.path.dirname(os.path.abspath(__file__))
    names_path = '../data/names.csv'
    names_path = os.path.join(current_path, names_path)
    with open(names_path, 'r') as file:
        names = file.read().splitlines()
        # Capitalize names
        names = [name.title() for name in names]

    for player_name in players_names:
        player_name_list = player_name.split()
        if len(player_name_list) < 3:
            # Split the name in spaces
            first_name = player_name_list[0]
            print("First name: ", first_name)
            # If first name not in names, remove player_name from players_names
            if first_name not in names:
                players_names.remove(player_name)
                print("Removed: ", player_name)

    return players_names

