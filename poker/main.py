import getopt
import time

import sys

from poker import Poker
from texas import TexasHoldemPoker
from texas_bot import TexasHoldemPokerBOT

if __name__ == "__main2__":
    # bankroll = [["bot_p", 10000], ["bot", 10000], ["bot2", 10000], ["bot3", 10000], ["bot4", 10000], ["bot5", 10000],
    #             ["bot6", 10000], ["bot7", 10000]]
    bankroll = [["Ban", 10000], ["bot_p_1", 10000]]
    total = sum([x[1] for x in bankroll])
    SB_position = 0
    tex = TexasHoldemPoker(bankroll)
    while len([x for x in bankroll if x[1] == total]) == 0:
        have_human = False
        if len([x for x in bankroll if "bot" not in x[0] and x[1] != 0]) != 0:
            have_human = True

        tex.start_round(SB_position, have_human)
        SB_position = (SB_position + 1) % len(bankroll)
        while bankroll[SB_position][1] == 0:
            SB_position = (SB_position + 1) % len(bankroll)
        print()
        if have_human:
            time.sleep(7)
    for ii in bankroll:
        print("%s:%d" % (ii[0], ii[1]), end=" ")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:p:o:", ["self=", "public=", "other="])
    except getopt.GetoptError:
        print('main.py -s <自已的> -p <公> -o <pk人数>')
        sys.exit(2)
    s = []
    pc = []
    other = 1
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <自已的> -p <公> -o <pk人数>')
            sys.exit()
        elif opt in ("-s", "--self"):
            s = Poker.get_poker_from_string(arg)
        elif opt in ("-p", "--public"):
            pc = Poker.get_poker_from_string(arg)
        elif opt in ("-o", "--other"):
            other = int(arg)

    # print("自牌:")
    # for i in s:
    #     Poker.print_show(i)
    print("\n公牌:")
    for i in pc:
        Poker.print_show(i)
    print("")
    poker = Poker()
    texas = TexasHoldemPoker([])
    poker.init_poker()
    poker.eliminate_card(s)
    poker.eliminate_card(pc)
    round_set = poker.poker_set_round
    w = 0
    draw = 0
    i = 0
    win_set = dict()
    for a in range(0, len(round_set)):
        for b in range(a + 1, len(round_set)):
            comb = [round_set[a], round_set[b]]
            r = texas.pk([pc + s, pc + comb])
            if r == 1:  # 猜的牌赢
                p_type, key = poker.jugg_type(pc + comb)
                if win_set.get(p_type) is None:
                    win_set[p_type] = []
                win_set.get(p_type).append(comb)
                w += 1
            i += 1

    card_type = ["同花顺", "四条", "葫芦", "同花", "顺子", "三条", "两对", "一对", "高牌"]
    for key in win_set:
        print("对方能赢的=== %s ===有：" % card_type[key])
        for a in win_set[key]:
            for b in a:
                poker.print_show(b)
            print(" | ",end="")
        print()

    print("对方可能的胜算: %d/%d=%f" % (w, i, w / i))
    # # 以下为算胜率
    # w = 0
    # draw = 0
    # i = 1
    # while True:
    #     w_t, draw_t, loss = TexasHoldemPokerBOT.win(pc, s, other, True)
    #     w += w_t
    #     draw += draw_t
    #     win = w / 5000 / i * 10000
    #     offer = draw / 5000 / i * 10000
    #     if other > 2:
    #         offer /= 2.5
    #     else:
    #         offer /= 2
    #     print("win:%d draw:%d result:%f" % (w, draw, win + offer))
    #     i += 1
