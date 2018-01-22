import random
import re


def start_game(player_set, bet_position):
    print("player:", end="")
    bot_count = 0
    for i in player_set:
        dice_temp = get_dice()
        i.append(dice_temp)
        if "bot" not in i[0]:
            print(i, end=",")
        else:
            bot_count += 1
    print()

    # call_set = [0] * len(player_set)
    # operation_history = [[]] * len(player_set) #这样的新建方式会导致[0] [1]所用的是同一个地址 2017.10.19 Ban
    call_set = []
    operation_history = []
    for temp in range(len(player_set)):
        call_set.append(0)
        operation_history.append([])

    enable_change = True
    while True:
        if "bot" in player_set[bet_position][0]:
            operation = thinking_random(call_set[bet_position - 1])
            print("%s operation:%s" % (player_set[bet_position][0], operation))
        else:
            operation = input("%s plz make u operation:" % player_set[bet_position][0])

        if "end" in operation:
            if call_set[(bet_position - 1) % len(player_set)] == 0:
                print("u cant end at the first")
            else:
                break
        else:
            result = re.findall(r'\d+', operation)
            if len(result) == 2:
                result = [int(x) for x in result]
                if result[1] not in range(1, 7):
                    print("r u fool? The dice's point only in 1 to 6")
                    continue
                elif result[1] == 1:
                    enable_change = False
                call_set[bet_position] = result[0] << 3 | result[1]
                if call_set[bet_position] <= call_set[bet_position - 1]:
                    print("u count of dice or point must more than last guy")
                else:
                    operation_history[bet_position].append(call_set[bet_position])
                    bet_position = (bet_position + 1) % len(player_set)
            else:
                print("unknown operation")

    lose = check_end(player_set, call_set[(bet_position - 1) % len(player_set)], enable_change)
    print(operation_history)
    return bet_position if lose else (bet_position - 1) % len(player_set)


def check_end(player_set, check_call, enable_change):
    count = check_call >> 3
    point = check_call & 7
    correct_count = 0

    for i in player_set:
        correct_count += len([x for x in i[1] if x == point])
        if enable_change and point != 1:
            correct_count += len([x for x in i[1] if x == 1])

    return count <= correct_count


def get_dice():
    dice = []
    for i in range(5):
        dice.append(random.randint(1, 6))
    return dice


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


if __name__ == "__main__":
    start_position = 0
    for i in range(50):
        player = [["Ban"], ["bot2"]]
        result_bet = start_game(player, start_position)
        print(player)
        print("%s lose!" % player[result_bet][0], end="\n")
        print()
        start_position = (start_position + 1) % len(player)
