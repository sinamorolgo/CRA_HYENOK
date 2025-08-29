import os

import pytest  # noqa
from pytest import fixture

from main import run, grade_factory, GoldGrade, SilverGrade, NormalGrade, Player, WeekdayEnum, Players, \
    FileManager, FILE_PATH, DataLine, Formatter, AttendanceManager, AbstractFileManager


def test_print_output(capsys):
    run()
    captured = capsys.readouterr()

    with open(r"C:\Users\User\PycharmProjects\CRA_HYENOK\results.txt") as f:
        expected = f.readlines()
    expected = ''.join(expected)
    expected = expected.replace("\n", "").replace(" ", "")
    captured = captured.out.replace("\n", "").replace(" ", "")
    assert ''.join(expected) == captured


def test_grade_factory():
    selected_grade = grade_factory(50)
    assert type(selected_grade) == GoldGrade
    assert selected_grade.__str__() == "GOLD"

    selected_grade = grade_factory(30)
    assert type(selected_grade) == SilverGrade
    assert selected_grade.__str__() == "SILVER"

    selected_grade = grade_factory(20)
    assert type(selected_grade) == NormalGrade
    assert selected_grade.__str__() == "NORMAL"


def test_player_cal_points():
    player = Player("hyenok", 1)
    player.cal_points(WeekdayEnum.monday)
    assert player.point == 1


def test_player_special_points():
    player = Player("hyenok", 1)
    player.dat[WeekdayEnum.wednesday] = 10
    player.dat[WeekdayEnum.saturday] = 10
    player.cal_special_points()
    assert player.point == 20


def test_player_grade():
    player = Player("hyenok", 1)
    player.point = 50
    player.cal_grade()

    assert type(player.grade) == GoldGrade


def test_players_get_player_add_if_new():
    players = Players()
    players.get_player_add_if_new("hyenok")
    assert players[1].name == "hyenok"


@fixture
def file_manager():
    return FileManager(FILE_PATH)


def test_file_manager_read_file(file_manager):
    if os.path.exists(FILE_PATH):
        assert len(file_manager.lines) > 0
    else:
        raise FileNotFoundError


def test_file_manager_parse_data(file_manager):
    parts = file_manager.parse_data("hyenok monday")
    assert parts.name == "hyenok"
    assert parts.weekday == "monday"


def test_file_manager_parse_data_raise(file_manager):
    with pytest.raises(ValueError):
        file_manager.parse_data("hyenok monday error")


def test_formatter_print_player_grade(capsys):
    player = Player("hyenok", 1)
    player.grade = GoldGrade()
    formatter = Formatter()

    formatter.print_player_grade(player)
    captured = capsys.readouterr()
    assert captured.out == f"NAME : {player.name}, POINT : {player.point}, GRADE : {player.grade}"


def test_formatter_separate_section_for_removing_print(capsys):
    formatter = Formatter()
    formatter.separate_section_for_removing_print()
    captured = capsys.readouterr()
    assert captured.out == "\nRemoved player\n==============\n"


class FakeFileManager(AbstractFileManager):
    def __init__(self, file_path):
        self.lines = ["hyenok monday"]
        pass

    def read_file(self):
        return ["hyenok monday"]

    def parse_data(self, file_name):
        return DataLine("hyenok", "monday")


def test_attendance_manager():
    players = Players()

    formatter = Formatter()
    file_manager = FakeFileManager("")

    manager = AttendanceManager(players, file_manager, formatter)
    manager.run()

    assert players[1].name == "hyenok"
    assert players[1].point == 1
