from collections import defaultdict
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Iterator

FILE_PATH = "attendance_weekday_500.txt"
MAX_PLAYERS = 100


class WeekdayEnum(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class AbstractPlayer(ABC):
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.dat = defaultdict(int)
        self.point = 0
        self.grade = -1
        self.wed = 0
        self.weekend = 0

    @abstractmethod
    def cal_points(self, weekday: WeekdayEnum):
        ...

    @abstractmethod
    def cal_special_points(self):
        ...

    @abstractmethod
    def cal_grade(self):
        ...


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


class AbstractPlayers(ABC):
    @abstractmethod
    def get_player_add_if_new(self, name: str)->AbstractPlayer:
        ...

    @abstractmethod
    def __iter__(self)->Iterator[AbstractPlayer]:
        ...

    @abstractmethod
    def __getitem__(self, id: int) -> AbstractPlayer:
        ...

    @property
    @abstractmethod
    def num_players(self) -> int:
        ...


class Players(AbstractPlayers):
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


@dataclass
class DataLine:
    name: str
    weekday: str


class AbstractFileManager(ABC):
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.lines: list[str] | None = None

    @abstractmethod
    def read_file(self):
        ...

    @staticmethod
    @abstractmethod
    def parse_data(line: str) -> DataLine:
        ...


class FileManager(AbstractFileManager):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.lines = self.read_file()

    def read_file(self):
        with open(self.file_path, encoding='utf-8') as f:
            return f.readlines()

    @staticmethod
    def parse_data(line: str) -> DataLine:
        parts = line.strip().split()
        if len(parts) != 2:
            raise ValueError
        return DataLine(name=parts[0], weekday=parts[1])


class AttendanceManager:
    def __init__(self, players: AbstractPlayers, file_manager: AbstractFileManager):
        self.players = players
        self.file_manager = file_manager

    def run(self):
        for line in self.file_manager.lines:
            parts = self.file_manager.parse_data(line)
            player = self.players.get_player_add_if_new(parts.name)
            player.cal_points(WeekdayEnum(parts.weekday))

        for player in self.players:
            player.cal_special_points()
            player.cal_grade()

        for id in range(1, self.players.num_players + 1):
            self.print_player_grade(id)

        self.separate_section_for_removing_print()
        for id in range(1, self.players.num_players + 1):
            if self.is_removing_candi(id):
                print(self.players[id].name)

    def print_player_grade(self, id: int):
        player = self.players[id]
        print(f"NAME : {player.name}, POINT : {player.point}, GRADE : ", end="")
        if player.grade == 1:
            print("GOLD")
        elif player.grade == 2:
            print("SILVER")
        else:
            print("NORMAL")

    def separate_section_for_removing_print(self):
        print("\nRemoved player")
        print("==============")

    def is_removing_candi(self, id):
        player = self.players[id]
        return player.grade not in (1, 2) and player.wed == 0 and player.weekend == 0


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


def run():
    players = Players()
    file_manager = FileManager(FILE_PATH)

    manager = AttendanceManager(players, file_manager)
    manager.run()


if __name__ == "__main__":
    run()
