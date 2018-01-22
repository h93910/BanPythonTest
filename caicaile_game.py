import os
import random
import re


# bot
def thinking_random(last_bet):
    count = last_bet >> 3
    point = last_bet & 7

    if count == 0:
        count = 2
        point = 1
    r = random.randint(0, 9)
    if r in range(4) and last_bet != 0:
        operation = "end"
    else:
        r = random.randint(0, 9)
        if r in range(3):
            count += random.randint(1, 2)
        else:
            point += random.randint(1, 2)
            if point - 6 > 0:
                point %= 6
                count += 1
        operation = "%d %d" % (count, point)

    return operation


last_coin = 0
last_bet_A = 1
last_bet_B_position = 0


# 只下A
def rush_A():
    global last_coin
    global last_bet_A

    if last_coin > coin:
        last_bet_A *= 2
    else:
        # last_bet_A = 1 * (coin // 4096 + 1)
        last_bet_A = 1
    if last_bet_A > coin:
        last_bet_A = coin
    last_coin = coin
    return str(last_bet_A)


# 只下B
def rush_BC():
    global last_coin
    global last_bet_B_position

    if last_coin > coin:
        last_bet_B_position += 1
    else:
        last_bet_B_position = 0

    if last_bet_B_position >= len(rush_b_bet):
        last_bet_B_position = len(rush_b_bet) - 1
    do_bet = rush_b_bet[last_bet_B_position]
    if do_bet > coin:
        do_bet = coin
    last_coin = coin
    return "0 " + str(do_bet)


# 只下D
def rush_D():
    # return "0 0 0 " + str(1)
    return "\n"


def thinking_primary(last_bet, my_dice, operation_hisstory, enable_change):
    go_call = 100  # 继续下的机率
    count = last_bet >> 3
    point = last_bet & 7
    definite_count = 0

    definite_count += len([x for x in my_dice if x == point])
    if enable_change and point != 1:
        definite_count += len([x for x in my_dice if x == 1])
    if definite_count >= count:
        go_call = 100


# 结算输入
def prior_settlement(o):
    global coin

    select = [0] * 4
    for i, j in enumerate(re.findall(r'\d+', o)):
        select[i] = int(j)
    coin -= sum(select)

    return select


# 小局结算
def settlement(player_s, r):
    global coin
    global earn_coin
    global A_count_round
    global B_count_round
    global C_count_round
    global D_count_round

    r = r[0]
    if sum(player_s) == 0:
        print("skip")
    else:
        if player_s[r] != 0:
            win_coin = player_s[r] * reward[r]
            print("u win coin:%d" % win_coin)
            coin += win_coin
            earn_coin += win_coin
        else:
            print("u lost:%d" % sum(player_s))

    save()
    result_letter = ""
    if r == 0:
        result_letter = "A"
        A_count_round += 1
    elif r == 1:
        result_letter = "B"
        B_count_round += 1
    elif r == 2:
        result_letter = "C"
        C_count_round += 1
    elif r == 3:
        result_letter = "D"
        D_count_round += 1

    for i in round_set:
        if len(i) != 12:
            i.append(result_letter)
            return


# 打印记分板
def print_scoreboard():
    if len(total_set) != 0:
        print("A:%d B:%d C:%d D:%d" % (total_set[-1][0], total_set[-1][1], total_set[-1][2], total_set[-1][3]))
    print("A:%d B:%d C:%d D:%d" % (A_count_round, B_count_round, C_count_round, D_count_round))
    print("[===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===]")
    for i in round_set:
        print(i)
    print("[===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===, ===]\n")


# 结束报告
def end_print(r):
    print("==============GAME OVER %d==================" % (r + 1))
    total_second = 0
    total_set.append([A_count_round, B_count_round, C_count_round, D_count_round])
    total_second += (len(total_set) - 1) * 60 * 60
    total_second += sum(total_set[-1]) * 50

    print("spending time:%dd%dh%dm%ds" % (
        total_second / 3600 // 24, total_second % 86400 // 3600, total_second % 3600 // 60, total_second % 60))
    print("%d round:" % len(total_set))
    for i in total_set[0:-1]:
        print(i)
    print("ending round:")
    print(total_set[-1])
    print("max coin:%d total earn:%d" % (max_coin, earn_coin))
    print("==============GAME OVER %d=================\n" % (r + 1))


# 保存数据
def save():
    with open(archive_path, 'w+') as text:
        output = str(coin)
        # text.truncate(0)
        # text.seek(0)
        text.write(output)


# 初始化数据
def init_data():
    global coin

    if os.path.exists(archive_path):
        print("load data")
        mode = "r"
    else:
        print("no save")
        mode = "w+"
    with open(archive_path, mode) as text:
        info = text.readline()
    if info != '':
        temp_coin = int(info)
        if temp_coin > 0:
            coin = temp_coin

if __name__ == "__main2__":
    print("r")

if __name__ == "__main__":
    mode = "ban"
    platform = "pc"
    chijizhi = 5900
    total_ball_count = 1000000

    A = 1607 / 46
    B = 1022 / 46
    C = 618 / 46
    D = 65 / 46
    ball_set = [0] * int(A / 72 * total_ball_count) + [1] * int(B / 72 * total_ball_count) + [2] * int(
        C / 72 * total_ball_count) + [3] * int(D / 72 * total_ball_count)

    ball_l = len(ball_set)
    if ball_l < total_ball_count:
        for temp in range(total_ball_count - ball_l):
            ball_set.append(0)

    reward = [2, 3, 6, 50]
    rush_b_bet = [1, 2, 3, 4, 6, 9, 14, 21, 31, 47, 70, 105, 158, 237, 305, 508, 762, 1143]

    if platform in "pc":
        archive_path = "ban_data_caicaile"
    elif platform in "android":
        archive_path = "sdcard/Ban/ban_data_caicaile"

    for jj in range(1):
        last_coin = 0
        last_bet_A = 1
        # =====统计信息===
        A_count_total = 0
        B_count_total = 0
        C_count_total = 0
        D_count_total = 0

        A_count_round = 0
        B_count_round = 0
        C_count_round = 0
        D_count_round = 0

        total_set = []
        round_set = []
        max_coin = 0
        earn_coin = 0
        # ====================
        for temp in range(6):
            round_set.append([])

        coin = 50
        init_data()
        if mode in "ban":
            operation = input("u coin:%d ,plz make u operation:" % coin)
        else:
            operation = rush_A()
            # operation = rush_B()
        end_all = False

        while "end" not in operation:
            if sum([A_count_round, B_count_round, C_count_round, D_count_round]) == 72:
                total_set.append([A_count_round, B_count_round, C_count_round, D_count_round])
                A_count_total += A_count_round
                B_count_total += B_count_round
                C_count_total += C_count_round
                D_count_total += D_count_round
                A_count_round = 0
                B_count_round = 0
                C_count_round = 0
                D_count_round = 0
                round_set = []
                for temp in range(6):
                    round_set.append([])

            if "ban" not in operation:
                player_select = prior_settlement(operation)
                result = random.sample(ball_set, 1)
                settlement(player_select, result)
                print_scoreboard()

                if coin > max_coin:
                    max_coin = coin
                if coin <= 0:
                    end_print(jj)
                    break
                elif coin >= chijizhi:
                    print("it is finish the task,earn coin:%d" % coin)
                    end_print(jj)
                    end_all = True
                    break

                if mode in "ban":
                    operation = input("u coin:%d ,plz make u operation:" % coin)
                else:
                    operation = rush_A()
                    # operation = rush_B()
                    # operation = rush_D()
                    print("bot coin:%d ,bot operation:%s" % (coin, operation))
            else:
                if "set_coin" in operation:
                    coin = int(operation.split(" ")[2])
                    operation = input("u coin:%d ,plz make u operation:" % coin)
                    # elif "reset" in operation:
                    #     save()
        else:
            end_all = True
        if end_all:
            end_print(jj)
            break
