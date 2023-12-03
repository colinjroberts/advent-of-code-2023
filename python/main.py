from p01 import p01
from p02 import p02

day_script_dict = {
    # 1: p01(),
    2: p02(),
}

if __name__ == '__main__':
    start, end = 2, 2
    for day in range(start, end+1):
        if day not in day_script_dict:
            raise KeyError("Day must be imported and added to day_script_dict before calling.")
        print(f"Day {day}: {day_script_dict[day]}")
