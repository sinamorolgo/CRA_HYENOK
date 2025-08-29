from collections import defaultdict
from enum import Enum
from dataclasses import dataclass

FILE_PATH = "attendance_weekday_500.txt"
MAX_PLAYERS = 100

players = {}

id_cnt = 0

# dat[사용자ID][요일]
dat = [defaultdict(int) for _ in range(MAX_PLAYERS)]
points = [0] * MAX_PLAYERS
grade = [0] * MAX_PLAYERS
names = [''] * MAX_PLAYERS
wed = [0] * MAX_PLAYERS
weekend = [0] * MAX_PLAYERS


class WeekdayEnum(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


@dataclass
class PointPolicy:
    point: int
    wednesday: int
    weekend: int


score_factory = {
    WeekdayEnum.monday: PointPolicy(1, 0, 0),
    WeekdayEnum.tuesday: PointPolicy(1, 0, 0),
    WeekdayEnum.wednesday: PointPolicy(3, 1, 0),
    WeekdayEnum.thursday: PointPolicy(1, 0, 0),
    WeekdayEnum.friday: PointPolicy(1, 0, 0),
    WeekdayEnum.saturday: PointPolicy(2, 0, 1),
    WeekdayEnum.sunday: PointPolicy(2, 0, 1),
}


def cal_points(name: str, weekday: str):
    global id_cnt

    add_player(name)
    cur_id = players[name]

    weekday_enum = WeekdayEnum(weekday)

    score_policy = score_factory[weekday_enum]
    points[cur_id] += score_policy.point
    wed[cur_id] += score_policy.wednesday
    weekend[cur_id] += score_policy.weekend

    dat[cur_id][weekday_enum] += 1


def add_player(w):
    global id_cnt
    if w not in players:
        id_cnt += 1
        players[w] = id_cnt
        names[id_cnt] = w


def read_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def run():
    try:
        lines = read_file(FILE_PATH)
        for line in lines:
            parts = parse_data(line)
            cal_points(name=parts[0], weekday=parts[1])

        for id in range(1, id_cnt + 1):
            cal_special_points(id)
            grade[id] = get_grade(points[id])

        for id in range(1, id_cnt + 1):
            print(f"NAME : {names[id]}, POINT : {points[id]}, GRADE : ", end="")
            if grade[id] == 1:
                print("GOLD")
            elif grade[id] == 2:
                print("SILVER")
            else:
                print("NORMAL")

        print("\nRemoved player")
        print("==============")
        for id in range(1, id_cnt + 1):
            if grade[id] not in (1, 2) and wed[id] == 0 and weekend[id] == 0:
                print(names[id])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


def get_grade(point):
    if point >= 50:
        return 1
    elif point >= 30:
        return 2
    else:
        return 0


def cal_special_points(id: int):
    if dat[id][WeekdayEnum.wednesday] > 9:
        points[id] += 10
    if dat[id][WeekdayEnum.saturday] + dat[id][WeekdayEnum.sunday] > 9:
        points[id] += 10


def parse_data(line):
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError
    return parts


if __name__ == "__main__":
    run()
