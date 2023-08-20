import datetime
import getopt
import sys
import time

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
    import random
    from paddleocr import PaddleOCR
    import os
    import numpy as np


    def my_print(s):
        log = False
        if log:
            print(s)


    # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    # ocr = PaddleOCR(use_angle_cls=True, use_gpu=True, lang="ch")
    """
        ALL IN
    """
    card_runners__open_raising_chart_bu = '22+,A2s+,K2s+,Q5s+,J7s+,T8s+,97s+,86s+,75s+,65s,A3o+,K9o+,Q9o+,J9o+,T8o+,98o'
    win_45_orc_bu = '22+,A2s+,K8s+,QTs+,A2o+,KTo+,QJo'
    win_35_orc_bu = '22+,A2s+,K2s+,Q2s+,J2s+,T3s+,95s+,84s+,74s+,63s+,53s+,43s,A2o+,K2o+,Q5o+,J8o+,T7o+,97o+,87o,76o,65o'  # 白给的范围

    texas = TexasHoldemPoker([])
    bot = TexasHoldemPokerBOT()
    my_range = texas.string_range_combine(win_45_orc_bu)
    free_range = texas.string_range_combine(win_35_orc_bu)

    w = True
    gg_set = None  # 存储gg游戏信息
    run_away = []
    while True:
        hwnd = 0
        rect = None
        if w:
            hwnd_set = bot.find_proccess('色')
            if gg_set is None:
                gg_set = [None] * len(hwnd_set)
            for i, hwnd in enumerate(hwnd_set):
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
                if True in [x > 120000 for x in gg.players_pool] and gg.my_pool < 10000:  # 实力差太大，直接换桌
                    if hwnd not in [x[0] for x in run_away]:
                        bot.click_scope_texts(im, '更换', rect, (0, 0.8, 0.3, 1))
                        run_away.append((hwnd, time.time() * 10 * 1000))
                    else:
                        for h in run_away:
                            if h[0] == hwnd and time.time() > h[1]:
                                run_away.remove(h)
                    continue  # 一定要换桌，不再操作
                if gg.my_cards == '':  # 没查到自己没有牌,等两秒再重新查
                    my_print('未查询到自己的牌')
                    bot.click_percent(0.42, 0.63, rect)
                    continue
                if gg_set[i] is not None and gg_set[i].my_cards == gg.my_cards and gg_set[i].played > 3:
                    my_print(f'{i} 已经操作过')  # 同一局且已经操作过了就不再操作
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
                played = False
                if my in my_range:  # call
                    played = bot.click_scope_texts(im, '全押', rect, (0.58, 0.72, 1, 1))
                else:  # fold
                    # 加入白给来混淆对手
                    chance = 3  # 20%的概率
                    # 生成0-99的随机整数
                    random_num = random.randint(0, 99)
                    # 判断随机数是否小于概率值
                    if random_num < chance and my in free_range:
                        print('白给的all in')
                        played = bot.click_scope_texts(im, '全押', rect, (0.58, 0.72, 1, 1))  # 概率事件触发
                    else:
                        played = bot.click_scope_texts(im, '弃牌', rect, (0.58, 0.72, 1, 1))  # 概率事件未触发
                if gg_set[i] is None or gg_set[i].my_cards != gg.my_cards:
                    gg_set[i] = gg
                gg_set[i].played += 1 if played else 0
                my_print(f'w {i} played:{gg_set[i].played}')
                # if w:
                #     im.save(str(gg) + '.jpg')
        else:
            # for i in [i for i in os.listdir('./') if 'jpg' in i]:
            #     im = Image.open(i)
            #     # 截取窗口并保存
            #     # bot.click_text(im, '弃牌', (0.698, 0.876, 0.773, 0.927), (100, 100, 500 500))
            #     gg = bot.get_gg_info(im)
            #     my = sorted(Poker.get_poker_from_string(gg.my_cards))
            #     print(gg)
            # print()

            # =================用于在Equilab中对比取胜率==================
            # p = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
            # t = []
            # for i in range(0, len(p)):
            #     for j in range(i, len(p)):
            #         t.append(p[i] + p[j])
            # pair = [x for x in t if x[0] == x[1]]
            # d = [x for x in t if x[0] != x[1]]
            # d1 = [x + 'o' for x in d]
            # d2 = [x + 's' for x in d]
            #
            # result = d1 + d2 + pair
            # w = []
            # for i in result:
            #     win = bot.win_from_pokerStra(i)
            #     if win > 35:
            #         w.append(i)
            # print(','.join(w))
            # ========== 用于在Equilab中对比取胜率 End==================

            # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
            for i in [i for i in os.listdir('./') if 'jpg' in i]:
                img = Image.open(i)
                t1 = time.time()
                # bot.click_scope_texts(img, '更换', [300, 400, 600, 800])
                # result = ocr.ocr(np.array(img), cls=True)
                bot.get_gg_info(img)
                bot.click_scope_texts(img, '全押', (300, 400), (0.58, 0.72, 1, 1))  # 概率事件触发
                print(time.time() - t1)
                # for line in result:
                #     # print(line[-1][0], line[-1][1])
                #     print(line)

            # try:
            #     gg = bot.get_gg_info(img)
            #     my_print(gg)
            # except Exception as e:
            #     print(e)
            #     continue
            # bot.click_text(img, '更换', (0.0, 0.78, 0.15, 0.95), None)
