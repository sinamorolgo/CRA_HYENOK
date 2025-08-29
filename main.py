from collections import defaultdict
from enum import Enum
from dataclasses import dataclass

FILE_PATH = "attendance_weekday_500.txt"
MAX_PLAYERS = 100

players_id = {}

id_cnt = 0



class WeekdayEnum(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.dat = defaultdict(int)
        self.point = 0
        self.grade = -1
        self.wed = 0
        self.weekend = 0

    def cal_points(self, weekday: WeekdayEnum):
        score_policy = score_factory[weekday]
        self.point += score_policy.point
        self.wed += score_policy.wednesday
        self.weekend += score_policy.weekend
        self.dat[weekday] += 1

    def cal_special_points(self):
        if self.dat[WeekdayEnum.wednesday] > 9:
            self.point += 10
        if self.dat[WeekdayEnum.saturday] + self.dat[WeekdayEnum.sunday] > 9:
            self.point += 10

    def cal_grade(self):
        if self.point >= 50:
            self.grade = 1
        elif self.point >= 30:
            self.grade = 2
        else:
            self.grade = 0


class Players:
    def __init__(self):
        self.players = defaultdict(None)
        self.map_id = defaultdict(int)

    def get_player_add_if_new(self, name: str):
        if not name in self.map_id:
            new_id = self.num_players + 1
            self.map_id[name] = new_id
            self.players[new_id] = Player(name, new_id)
        return self.players[self.map_id[name]]

    @property
    def num_players(self):
        return len(self.players)

    def __iter__(self):
        return iter(self.players.values())

    def __getitem__(self, id):
        return self.players[id]


players = Players()


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


def read_file(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def add_player_if_new(name: str):
    global id_cnt
    if name not in players_id:
        id_cnt += 1
        players_id[name] = id_cnt
        names[id_cnt] = name


def cal_points(name: str, weekday: str):
    player = players.get_player_add_if_new(name)
    player.cal_points(WeekdayEnum(weekday))


def separate_section_for_removing_print():
    print("\nRemoved player")
    print("==============")


def is_removing_candi(id):
    player = players[id]

    return player.grade not in (1, 2) and player.wed == 0 and player.weekend == 0


def print_player_grade(id):
    player = players[id]
    print(f"NAME : {player.name}, POINT : {player.point}, GRADE : ", end="")
    if player.grade == 1:
        print("GOLD")
    elif player.grade == 2:
        print("SILVER")
    else:
        print("NORMAL")


def get_grade(point):
    if point >= 50:
        return 1
    elif point >= 30:
        return 2
    else:
        return 0


def parse_data(line):
    parts = line.strip().split()
    if len(parts) != 2:
        raise ValueError
    return parts


def run():
    try:
        lines = read_file(FILE_PATH)
    except FileNotFoundError:
        raise ("파일을 찾을 수 없습니다.")

    for line in lines:
        parts = parse_data(line)
        cal_points(name=parts[0], weekday=parts[1])

    for player in players:
        player.cal_special_points()
        player.cal_grade()

    for id in range(1, players.num_players + 1):
        print_player_grade(id)

    separate_section_for_removing_print()
    for id in range(1, players.num_players + 1):
        if is_removing_candi(id):
            print(players[id].name)


if __name__ == "__main__":
    run()
