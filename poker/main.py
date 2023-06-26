import datetime
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

if __name__ == "__main__1":
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
            print(" | ", end="")
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

if __name__ == "__main__2":
    # pc = Poker.get_poker_from_string("4dTs6s")
    pc = []
    other = 1
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
    poker.eliminate_card(pc)
    round_set = poker.poker_set_round
    play_range = [['As3h'], texas.string_range_combine(
        "99+, AJs+, KQs, AQo+")]
    # play_range = [['KdKs'], ['KhKc']]

    # 以下为算胜率
    w = 0
    draw = 0
    i = 1
    while True:
        w_t, draw_t, loss = TexasHoldemPokerBOT.win_range_monte_carlo(pc, play_range)
        w += w_t
        draw += draw_t
        win = w / 5000 / i * 10000
        offer = draw / 5000 / i * 10000
        if other > 2:
            offer /= 2.5
        else:
            offer /= 2
        print("win:%d draw:%d result:%f" % (w, draw, win + offer))
        i += 1

if __name__ == "__main__":
    from PIL import ImageGrab, Image
    import win32con, win32gui
    from ctypes import wintypes
    import ctypes
    import re
    import pyautogui


    def my_print(s):
        log = False
        if log:
            print(s)


    """
        ALL IN
    """
    card_runners__open_raising_chart_bu = '22+,A2s+,K2s+,Q5s+,J7s+,T8s+,97s+,86s+,75s+,65s,A3o+,K9o+,Q9o+,J9o+,T8o+,98o'

    texas = TexasHoldemPoker([])
    bot = TexasHoldemPokerBOT()
    my_range = texas.string_range_combine(card_runners__open_raising_chart_bu)
    w = True
    while True:
        hwnd = 0
        rect = None
        if w:
            hwnd_set = bot.find_proccess('色')

            for hwnd in hwnd_set:
                # 截取窗口并保存
                rect = bot.get_window_pos(hwnd)
                # 发送还原最小化窗口的信息
                win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                # 将目标窗口移到最前面
                win32gui.SetForegroundWindow(hwnd)

                im = ImageGrab.grab(rect)
                try:
                    gg = bot.get_gg_info(im)
                    my_print(gg)
                except Exception as e:
                    print(e)
                    continue
                if gg.my_pool > 150000:
                    bot.recycle_coin(rect)
                if gg.my_cards == '':  # 没查到自己没有牌,等两秒再重新查
                    my_print('未查询到自己的牌,休息两秒')
                    bot.click_percent(0.42, 0.63, rect)
                    continue

                # 点pokerStra
                # try:
                #     win = bot.win_from_pokerStra(gg.my_cards)
                # except Exception as e:
                #     my_print('没复制到结果')
                #     continue
                my = sorted(Poker.get_poker_from_string(gg.my_cards))

                if rect is None or w is False:
                    my_print('没取到窗口的rect')
                    continue
                # 发送还原最小化窗口的信息
                win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                # 将目标窗口移到最前面
                win32gui.SetForegroundWindow(hwnd)
                if my in my_range:  # call
                    bot.click_text(im, '全押', (0.866, 0.875, 0.945, 0.922), rect)
                else:  # fold
                    bot.click_text(im, '弃牌', (0.698, 0.876, 0.773, 0.927), rect)
                # if w:
                #     im.save(str(gg) + '.jpg')
        else:
            im = Image.open(
                """poker23.jpg""")
            # 截取窗口并保存
            # bot.click_text(im, '弃牌', (0.698, 0.876, 0.773, 0.927), (100, 100, 500 500))
            gg = bot.get_gg_info(im)
            my = sorted(Poker.get_poker_from_string(gg.my_cards))
            print(gg)
