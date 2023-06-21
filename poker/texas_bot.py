import random
from itertools import combinations, product
import numpy as np
from dataclasses import dataclass, field
from PIL import ImageGrab, Image
import win32con, win32gui
from ctypes import wintypes
import ctypes
import pytesseract
import re
import cv2

from poker import Poker


class TexasHoldemPokerBOT:
    def __init__(self):
        pass

    def thinking_primary(self, can_bet, can_check, bb, public_cards, plays_cards, other_on_play_count, pool,
                         single_pool, have_human):
        operation_set = ['check', "flat", "fold", "raise", "all in"]
        win = TexasHoldemPokerBOT.win(public_cards, plays_cards, other_on_play_count)
        if have_human is False:
            print("win:%d" % win)
        stage = len(public_cards + plays_cards)
        if stage == 2:  # pre-flop
            if win in range(4150):
                if can_check:
                    return operation_set[0]
                else:
                    if max(single_pool) > bb:
                        return operation_set[2]
                    else:
                        r = random.randint(0, 100)
                        if r in range(71):
                            return operation_set[2]
                        else:
                            return operation_set[1]
            else:
                r = random.randint(0, 100)
                if can_check:
                    if r in range(int(-(win // 100) + 120)):
                        return operation_set[0]
                    else:
                        if can_bet // bb >= 1:
                            bet = random.randint(1, 4 if can_bet // bb >= 5 else can_bet // bb) * bb
                            if bet >= can_bet:
                                return operation_set[-1]
                            operation = operation_set[3] + ":" + str(int(bet))
                            return operation
                        else:
                            return operation_set[-1]
                else:
                    max_bet_of_bb = max(single_pool) // bb
                    my_bet_of_bb = can_bet // bb
                    if max_bet_of_bb / my_bet_of_bb > 0.6:
                        if r in range(80):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    else:
                        if r in range(30):
                            return operation_set[1]
                        else:
                            if can_bet // bb >= 1:
                                bet = max(single_pool) + \
                                      random.randint(1, 3 if can_bet // bb >= 3 else can_bet // bb) * bb
                                if bet >= can_bet:
                                    return operation_set[-1]
                                operation = operation_set[3] + ":" + str(int(bet))
                                return operation
                            else:
                                return operation_set[-1]
        elif stage == 5 or stage == 6:  # flop
            if win in range(1500):
                if can_check:
                    return operation_set[0]
                else:
                    return operation_set[2]
            elif win in range(1500, 3000):
                r = random.randint(0, 100)
                max_bet_of_bb = max(single_pool) // bb
                my_bet_of_bb = can_bet // bb
                ratio = max_bet_of_bb / my_bet_of_bb
                if can_check:
                    if r in range(int(-(win // 100) + 105)):
                        return operation_set[0]
                    else:
                        if ratio < 0.3:
                            return operation_set[1]
                        else:
                            return operation_set[2]
                else:
                    if ratio > 0.5:
                        if r in range(90):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    else:
                        if r in range(int((win // 100) + 10)):
                            return operation_set[1]
                        else:
                            return operation_set[2]
            else:
                r = random.randint(0, 100)
                if can_check:
                    if r in range(int(-2.1 * (win // 100) + 215)):
                        return operation_set[0]
                    else:
                        if can_bet // bb >= 1:
                            bet = random.randint(1, 10 if can_bet // bb >= 10 else can_bet // bb) * bb
                            if bet >= can_bet:
                                return operation_set[-1]
                            operation = operation_set[3] + ":" + str(int(bet))
                            return operation
                        else:
                            return operation_set[-1]
                else:
                    max_bet_of_bb = max(single_pool) // bb
                    my_bet_of_bb = can_bet // bb
                    ratio = max_bet_of_bb / my_bet_of_bb
                    if ratio > 0.9:
                        if r in range(int(-2 * (win // 100) + 205)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    elif ratio * 100 in range(70, 90):
                        if r in range(int(-1.8 * (win // 100) + 185)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    elif ratio * 100 in range(30, 70):
                        if r in range(int(-1.1 * (win // 100) + 113)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    else:
                        if r in range(int(-1.2 * (win // 100) + 130)):
                            return operation_set[1]
                        else:
                            if can_bet // bb >= 1:
                                bet = max(single_pool) + \
                                      random.randint(1, 8 if can_bet // bb >= 8 else can_bet // bb) * bb
                                if bet >= can_bet:
                                    return operation_set[-1]
                                operation = operation_set[3] + ":" + str(int(bet))
                                return operation
                            else:
                                return operation_set[-1]
                                # elif stage == 6:  # turn
                                #     pass
        elif stage == 7:  # river
            r = random.randint(0, 100)
            ratio = 0
            if can_check is False:
                max_bet_of_bb = max(single_pool) // bb
                my_bet_of_bb = can_bet // bb
                ratio = max_bet_of_bb / my_bet_of_bb

            if win in range(9800, 10001):
                return operation_set[-1]
            elif win in range(8000, 9800):
                if can_check:
                    if r in range(int(-(win // 100) + 100)):
                        return operation_set[0]
                    else:
                        if can_bet // bb >= 1:
                            bet = random.randint(1, 8 if can_bet // bb >= 8 else can_bet // bb) * bb
                            if bet >= can_bet:
                                return operation_set[-1]
                            operation = operation_set[3] + ":" + str(int(bet))
                            return operation
                        else:
                            return operation_set[-1]
                else:
                    if ratio < 1:
                        if r in range(int(-2 * (win // 100) + 260 - 7 / ratio)):
                            return operation_set[1]
                        else:
                            if can_bet // bb >= 1:
                                bet = max(single_pool) + \
                                      random.randint(1, 3 if can_bet // bb >= 3 else can_bet // bb) * bb
                                if bet >= can_bet:
                                    return operation_set[-1]
                                operation = operation_set[3] + ":" + str(int(bet))
                                return operation
                            else:
                                return operation_set[-1]
                    else:
                        if r in range(90):
                            return operation_set[-1]
                        else:
                            return operation_set[2]
            elif win in range(7000, 8000):
                if can_check:
                    if r in range(int(-0.5 * (win // 100) + 90)):
                        return operation_set[0]
                    else:
                        if can_bet // bb >= 1:
                            bet = random.randint(1, 3 if can_bet // bb >= 8 else can_bet // bb) * bb
                            if bet >= can_bet:
                                return operation_set[-1]
                            operation = operation_set[3] + ":" + str(int(bet))
                            return operation
                        else:
                            return operation_set[-1]
                else:
                    if ratio < 1:
                        if r in range(int(-1.5 * (win // 100) + 190 - 7 / ratio)):
                            return operation_set[1]
                        else:
                            if can_bet // bb >= 1:
                                bet = max(single_pool) + \
                                      random.randint(1, 3 if can_bet // bb >= 3 else can_bet // bb) * bb
                                if bet >= can_bet:
                                    return operation_set[-1]
                                operation = operation_set[3] + ":" + str(int(bet))
                                return operation
                            else:
                                return operation_set[-1]
                    else:
                        if r in range(30):
                            return operation_set[-1]
                        else:
                            return operation_set[2]
            elif win in range(3000, 7000):
                if can_check:
                    return operation_set[0]
                else:
                    if ratio < 0.3:
                        if r in range(int(-(win // 100) + 80)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    else:
                        if r in range(int(-(win // 100) + 110)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
            else:
                if can_check:
                    return operation_set[0]
                else:
                    if ratio < 0.2:
                        if r in range(int(-2 * (win // 100) + 100)):
                            return operation_set[2]
                        else:
                            return operation_set[1]
                    else:
                        return operation_set[2]

    def thinking_random(self, can_bet, can_check, bb):
        operation_set = ['check', "flat", "fold", "raise", "all in"]
        weights = [30, 5, 2, 2, 1]

        if can_check:
            del operation_set[2]
            del weights[2]
        else:
            operation_set = operation_set[1:-1]
            weights = weights[1:-1]

        operation = ""
        r = random.randint(1, sum(weights))
        i = 1
        while i <= len(weights):
            if r <= sum(weights[0:i]):
                operation = operation_set[i - 1]
                break
            i += 1
        if operation == "raise":
            if can_bet > bb:
                operation += ":%d" % random.randrange(bb, can_bet, bb)
            else:
                print("bot cant raise,so only all in")
                operation = "all in"

        return operation

    @staticmethod
    def win(public_cards, plays_cards, other_on_play_count, cumulate=False):
        # count = self.C(50, 5 + 2 * other_on_play_count)
        count = 5000

        leftover = Poker.get_poker_set()
        for i in public_cards:
            leftover.remove(i)
        for i in plays_cards:
            leftover.remove(i)

        win = 0
        draw = 0
        lose = 0
        for i in range(count):
            left = leftover.copy()
            communicate = public_cards.copy()
            all_players_card = list()
            all_players_card.append(plays_cards)
            # 补全
            while len(communicate) < 5:
                r = random.randint(0, len(left) - 1)
                communicate.append(left[r])
                del left[r]
            # 随
            for j in range(other_on_play_count):
                temp_card = list()
                for k in range(2):
                    r = random.randint(0, len(left) - 1)
                    temp_card.append(left[r])
                    del left[r]
                all_players_card.append(temp_card)

            pk_set = list()
            for j in range(len(all_players_card)):
                player_combination = Poker.jugg_type(communicate + list(all_players_card[j]))
                # print("%d:%s" % (j, TexasHoldemPoker.card_type(player_combination)))
                pk_set.append(player_combination)
            pk_result_set = sorted(pk_set, key=lambda x: (-x[0], x[1]))
            # print("max:%s" % self.card_type(max_p))

            # winners = []
            # for j in range(len(pk_set)):
            #     if pk_set[j] == max_p:
            #         winners.append(j)
            # if len(winners) == 1 and winners[0] == 0:
            #     win += 1
            if pk_set[0] == pk_result_set[-1]:
                if len(pk_set) > 1 and pk_set[0] == pk_result_set[-2]:
                    draw += 1
                else:
                    win += 1
            else:
                lose += 1

        result = int(win / count * 10000)
        if cumulate is False:
            return result
        else:
            return win, draw, lose

    @staticmethod
    def win_range_monte_carlo(public_cards, plays_cards, count=20000):
        '''
        按范围的蒙特卡罗猜胜率万分比
        :param public_cards: 公牌数组　[]
        :param plays_cards:  选手的卡池选择范围或指定牌数组 [[一号玩家范围],[二号玩家　范围]]　如玩家范围为空数组则为全随机
        :param count: 查多少轮 默认三十万
        :return:
        '''

        leftover = Poker.get_poker_set()
        for i in public_cards:  # 先移除公牌
            leftover.remove(i)

        win = [0] * len(plays_cards)
        draw = [0] * len(plays_cards)
        lose = [0] * len(plays_cards)

        all_players_card_stable = [[]] * len(plays_cards)
        # 先把明确的选手卡池中抽卡
        for j in range(len(plays_cards)):
            if len(plays_cards[j]) != 0 and any(c in plays_cards[j][0] for c in 'dchs'):  # 是否是确认的手牌
                temp_card = Poker.get_poker_from_string(plays_cards[j][0])
                for k in temp_card:
                    leftover.remove(k)
                all_players_card_stable[j] = temp_card

        # 开始模拟
        for i in range(count):
            left = leftover.copy()
            communicate = public_cards.copy()

            all_players_card = all_players_card_stable.copy()
            # 先随机中抽卡
            for j in range(len(plays_cards)):
                if len(plays_cards[j]) == 0:  # 全随机
                    temp_card = list()
                    for k in range(2):
                        r = random.randint(0, len(left) - 1)
                        temp_card.append(left[r])
                        del left[r]
                    all_players_card[j] = temp_card

            # 再抽范围的牌
            for j in range(len(plays_cards)):
                if len(plays_cards[j]) != 0:
                    if any(c in plays_cards[j][0] for c in 'dchs') is False:
                        # 移除已经不存在的组合
                        play_range = list(filter(lambda x: x[0] in left and x[1] in left, plays_cards[j].copy()))
                        temp_card = random.choice(play_range)
                        for k in temp_card:
                            left.remove(k)
                        all_players_card[j] = temp_card

            # 将公牌补齐
            while len(communicate) < 5:
                r = random.randint(0, len(left) - 1)
                communicate.append(left[r])
                del left[r]

            pk_set = list()
            for j in range(len(all_players_card)):
                player_combination = Poker.jugg_type(communicate + list(all_players_card[j]))
                pk_set.append(player_combination)
            pk_result_set = sorted(pk_set, key=lambda x: (-x[0], x[1]))
            # if pk_result_set[0][0] != pk_result_set[1][0]:# win
            # if pk_result_set[0][0] == pk_result_set[1][0] and pk_result_set[0][1] != pk_result_set[1][1]:# draw
            #     print(pk_result_set)
            #     for k in communicate:
            #         Poker.print_show(k)
            #     print()

            for p in range(len(pk_set)):
                split = pk_result_set.count(pk_result_set[-1])  # 非零则存在平局且需要划分多少份
                if pk_set[p] == pk_result_set[-1]:
                    if split != 1:
                        draw[p] += 1 / split
                    else:
                        win[p] += 1
                else:
                    lose[p] += 1

            if i % 10000 == 0:
                result = (np.array(win) + np.array(draw)) / (i + 1) * 10000
                print(f'{i + 1} {result}')

        result = (np.array(win) + np.array(draw)) / count * 10000
        print(f'result:{result}')
        print(f'win:{(np.array(win)) / count * 10000}')
        print(f'draw:{(np.array(draw)) / count * 10000}')
        return result

    @staticmethod
    def win_range_exhaustion(public_cards, plays_cards):
        '''
        按范围的穷举胜率
        :param public_cards: 公牌数组　[]
        :param plays_cards:  选手的卡池选择范围或指定牌数组 [[一号玩家范围],[二号玩家　范围]]　如玩家范围为空数组则为全随机
        :return:
        '''
        count = 1

        leftover = Poker.get_poker_set()
        for i in public_cards:  # 去掉公牌
            leftover.remove(i)

        win = [0] * len(plays_cards)
        draw = [0] * len(plays_cards)
        lose = [0] * len(plays_cards)

        left = leftover.copy()
        communicate = public_cards.copy()  # 公牌的所有可能组合
        all_players_card = [[]] * len(plays_cards)

        for j in range(len(plays_cards)):
            if len(plays_cards[j]) != 0:
                if any(c in plays_cards[j][0] for c in 'dchs'):  # 是否是确认的手牌
                    temp_card = Poker.get_poker_from_string(plays_cards[j][0])
                    for k in temp_card:
                        left.remove(k)  # 先把明确的选手卡池中抽卡
                    all_players_card[j] = [temp_card]
                else:
                    # 移除已经不存在的组合
                    play_range = [x for x in plays_cards[j] if x[0] in left and x[1] in left]
                    all_players_card[j] = play_range
            else:  # 全随机的话
                all_players_card[j] = combinations(left, 2)  # 从剩下的牌中取两张的全部组合

        # 补全
        if len(communicate) < 5:
            communicate = np.array(list(combinations(left, 5 - len(communicate))))
            for i in public_cards:
                communicate = np.insert(communicate, 0, i, axis=1)
        else:
            communicate = [communicate]

        '''
            2023年6月15日放弃此方法的编写，当玩家到达三个时，穷举的数量太巨大
        '''
        set_combine = communicate.copy()  # 一组公组与玩家牌的全部穷举
        for p in all_players_card:
            set_combine = list(product(set_combine, p))
        # 再抽范围的牌
        for j in range(len(plays_cards)):
            if len(plays_cards[j]) != 0:
                if any(c in plays_cards[j][0] for c in 'dchs') is False:
                    # 移除已经不存在的组合
                    play_range = list(filter(lambda x: x[0] in left and x[1] in left, plays_cards[j].copy()))
                    temp_card = random.choice(play_range)
                    for k in temp_card:
                        left.remove(k)
                    all_players_card[j] = temp_card

        pk_set = list()
        for j in range(len(all_players_card)):
            player_combination = Poker.jugg_type(communicate + list(all_players_card[j]))
            pk_set.append(player_combination)
        pk_result_set = sorted(pk_set, key=lambda x: (-x[0], x[1]))
        # if pk_result_set[0][0] != pk_result_set[1][0]:# win
        # if pk_result_set[0][0] == pk_result_set[1][0] and pk_result_set[0][1] != pk_result_set[1][1]:# draw
        #     print(pk_result_set)
        #     for k in communicate:
        #         Poker.print_show(k)
        #     print()

        for p in range(len(pk_set)):
            split = pk_result_set.count(pk_result_set[-1])  # 非零则存在平局且需要划分多少份
            if pk_set[p] == pk_result_set[-1]:
                if split != 1:
                    draw[p] += 1 / split
                else:
                    win[p] += 1
            else:
                lose[p] += 1

        if i % 100 == 0:
            result = (np.array(win) + np.array(draw)) / (i + 1) * 10000
            print(result)

        result = (np.array(win) + np.array(draw)) / count * 10000
        print(f'result:{result}')
        print(f'win:{(np.array(win)) / count * 10000}')
        print(f'draw:{(np.array(draw)) / count * 10000}')
        # if cumulate is False:
        #     return result
        # else:
        #     return win, draw, lose

    def get_window_pos(self, hwnd):
        '''
            获取窗口的坐标
        :param hwnd:
        :return:
        '''
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(hwnd),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            return rect.left, rect.top, rect.right, rect.bottom
        except WindowsError as e:
            raise e

    def get_card_info_from_pic(self, region):
        config = r'-c tessedit_char_whitelist=23456789TJQKAdchs --psm 6 -l poker'
        result = pytesseract.image_to_string(region, config=config)
        if len(result) == 0:
            return None
        card = result.split('\n')
        if len(card) != 3:
            n = result.replace('\n', '')
            region.save(f'{n}_{random.randint(0, 5)}.png')
            return None
        if card[0][0:2] == '10':
            number = "T"
        else:
            number = card[0].strip()[0]
        back = number + card[1][0]
        if any(c in back[1] for c in 'dchs'):
            return back
        return None

    def get_gg_info(self, pic):
        gg = GGGameInfo()

        w, h = pic.size
        # 查自己的池
        region = pic.crop((int(w * 0.44), int(h * 0.905), int(w * 0.565), int(h * 0.942)))
        # 识别文字中的时间，用于保存文字名
        text = pytesseract.image_to_string(region)
        pattern = re.compile(r'(.)(\d{1,3}[,\d{3}]*.\d+)')
        search = re.search(pattern, text)
        if search is not None:
            gg.my_pool = float(search.group(2).replace(',', ''))

        # 查自己的手牌
        card1 = pic.crop((int(w * 0.44), int(h * 0.748), int(w * 0.469), int(h * 0.828))).convert('RGBA').rotate(-8)
        card2 = pic.crop((int(w * 0.49), int(h * 0.74), int(w * 0.519), int(h * 0.821)))
        card1_result = self.get_card_info_from_pic(card1)
        card2_result = self.get_card_info_from_pic(card2)
        if card1_result is not None:
            gg.my_cards = card1_result + card2_result
        # 公牌
        card1 = pic.crop((int(w * 0.298), int(h * 0.415), int(w * 0.322), int(h * 0.493)))
        card2 = pic.crop((int(w * 0.38), int(h * 0.415), int(w * 0.41), int(h * 0.493)))
        card3 = pic.crop((int(w * 0.467), int(h * 0.415), int(w * 0.495), int(h * 0.493)))
        card4 = pic.crop((int(w * 0.552), int(h * 0.415), int(w * 0.580), int(h * 0.493)))
        card5 = pic.crop((int(w * 0.635), int(h * 0.415), int(w * 0.662), int(h * 0.493)))
        l = [self.get_card_info_from_pic(x) for x in [card1, card2, card3, card4, card5]]
        gg.public_cards = l

        # 底池
        region = pic.crop((int(w * 0.39), int(h * 0.368), int(w * 0.65), int(h * 0.405)))
        # 识别文字中的时间，用于保存文字名
        config = r'--psm 6 -l eng'
        text = pytesseract.image_to_string(region, config=config)
        pattern = re.compile(r'(.)(\d{1,3}[,\d{3}]*.\d+)')
        gg.pool = float(re.search(pattern, text).group(2).replace(',', ''))

        print(gg)
        return gg

    def click(self, x, y):

        pass


@dataclass
class GGGameInfo:
    my_pool: float = 0.0
    my_cards: str = ""
    public_cards: list = None
    pool: float = 0.0
