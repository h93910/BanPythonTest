# import time
# import os
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.chdir(BASE_DIR)

# if __name__ == "__main__":
#     from .texas import TexasHoldemPoker
#
#     bankroll = [["Ban", 10000], ["bot", 10000], ["bot2", 10000], ["bot3", 10000], ["bot4", 10000], ["bot5", 10000],
#                 ["bot6", 10000], ["bot7", 10000]]
#     total = sum([x[1] for x in bankroll])
#     SB_position = 0
#     tex = TexasHoldemPoker(bankroll)
#     while len([x for x in bankroll if x[1] == total]) == 0:
#         have_human = False
#         if len([x for x in bankroll if "bot" not in x[0] and x[1] != 0]) != 0:
#             have_human = True
#
#         tex.start_round(SB_position, have_human)
#         SB_position = (SB_position + 1) % len(bankroll)
#         while bankroll[SB_position][1] == 0:
#             SB_position = (SB_position + 1) % len(bankroll)
#         print()
#         if have_human:
#             time.sleep(7)
#     for ii in bankroll:
#         print("%s:%d" % (ii[0], ii[1]), end=" ")

from bantest.poker.texas_bot import TexasHoldemPokerBOT
from bantest.poker.texas import TexasHoldemPoker
from bantest.poker.poker import Poker
import threading
import time

ttt = TexasHoldemPoker(None)

c = 100000
win = 0
lose = 0
draw = 0


def cal():
    global win, draw, lose
    for j in range(c // 100):
        r = ttt.test()
        if r == -1:
            win += 1
        elif r == 0:
            draw += 1
        else:
            lose += 1


def test1():
    global win, draw, lose
    public = []
    play = [2, 3, 0x34, 5, 0x37, 14]
    # result = Poker.jugg_type(play)
    # print(result)
    # for i in result[1]:
    #     print(Poker.switch_poker_number(i))

    last = time.time() * 100

    # threads = []
    # for i in range(1000):
    #     threads.append(threading.Thread(target=cal))
    #
    # for t in threads:
    #     t.start()
    #     t.join()

    for i in range(c):
        r = ttt.test()
        if r == -1:
            win += 1
        elif r == 0:
            draw += 1
        else:
            lose += 1

    print("finish", time.time() * 1000 - last)
    print("win:%d lose:%d draw:%d" % (win, lose, draw))



    # temp = TexasHoldemPokerBOT().win(public, play, 1)
    # for j in range(12):
    #     last = 0
    #     first = 0
    #     play[1] += 1
    #     for i in range(1, 20):
    #         # now = \
    #         temp = TexasHoldemPokerBOT().win(public, play, i)

    # if i == 1:
    #     first = temp
    # else:
    #     # t = 7024.3 * (i + 1) ** (-0.884)
    #     t = 7518.4 * (i + 1) ** (-0.911)
    #     print(t)
    #     print("误差:%f" % (abs(temp - t) / temp))

    # if last != 0:
    #     print(last - now)
    # else:
    #     print(now)
    # last = now
    #
    # print()


if __name__ == "__main__":
    test1()
