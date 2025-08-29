players = {}
id_cnt = 0

MAX_PALYERS = 100

# dat[사용자ID][요일]
dat = [[0] * MAX_PALYERS for _ in range(MAX_PALYERS)]
points = [0] * MAX_PALYERS
grade = [0] * MAX_PALYERS
names = [''] * MAX_PALYERS
wed = [0] * MAX_PALYERS
weeken = [0] * MAX_PALYERS


def cal_score(name: str, weekday: str):
    global id_cnt

    add_player(name)
    cur_id = players[name]

    add_point = 0
    index = 0

    if weekday == "monday":
        index = 0
        add_point += 1
    elif weekday == "tuesday":
        index = 1
        add_point += 1
    elif weekday == "wednesday":
        index = 2
        add_point += 3
        wed[cur_id] += 1
    elif weekday == "thursday":
        index = 3
        add_point += 1
    elif weekday == "friday":
        index = 4
        add_point += 1
    elif weekday == "saturday":
        index = 5
        add_point += 2
        weeken[cur_id] += 1
    elif weekday == "sunday":
        index = 6
        add_point += 2
        weeken[cur_id] += 1

    dat[cur_id][index] += 1
    points[cur_id] += add_point


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
                    cal_score(parts[0], parts[1])

        for i in range(1, id_cnt + 1):
            if dat[i][2] > 9:
                points[i] += 10
            if dat[i][5] + dat[i][6] > 9:
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
            if grade[i] not in (1, 2) and wed[i] == 0 and weeken[i] == 0:
                print(names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    input_file()
