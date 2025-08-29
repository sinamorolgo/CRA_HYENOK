from collections import defaultdict
from enum import Enum
from dataclasses import dataclass

players = {}

id_cnt = 0

MAX_PALYERS = 100

# dat[사용자ID][요일]
dat = [defaultdict(int) for _ in range(MAX_PALYERS)]
points = [0] * MAX_PALYERS
grade = [0] * MAX_PALYERS
names = [''] * MAX_PALYERS
wed = [0] * MAX_PALYERS
weekend = [0] * MAX_PALYERS


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


def input_file():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    cal_points(parts[0], parts[1])

        for i in range(1, id_cnt + 1):
            if dat[i][WeekdayEnum.wednesday] > 9:
                points[i] += 10
            if dat[i][WeekdayEnum.saturday] + dat[i][WeekdayEnum.sunday] > 9:
                points[i] += 10

            if points[i] >= 50:
                grade[i] = 1
            elif points[i] >= 30:
                grade[i] = 2
            else:
                grade[i] = 0

            print(f"NAME : {names[i]}, POINT : {points[i]}, GRADE : ", end="")
            if grade[i] == 1:
                print("GOLD")
            elif grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")

        print("\nRemoved player")
        print("==============")
        for i in range(1, id_cnt + 1):
            if grade[i] not in (1, 2) and wed[i] == 0 and weekend[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()
