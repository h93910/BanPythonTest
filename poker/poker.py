import random
from collections import Counter


class Poker:
    def __init__(self):
        self.poker_set = []
        for i in range(0, 4):
            self.poker_set += [x | (0x10 * i) for x in [x for x in range(2, 15)]]

    def init_poker(self):
        self.poker_set_round = self.poker_set.copy()

    def get_card(self, count):
        '''
        发牌
        :param count: 发多少张
        '''
        card = []
        for i in range(count):
            r = random.randint(0, len(self.poker_set_round) - 1)
            card.append(self.poker_set_round[r])
            del self.poker_set_round[r]
        return card

    def eliminate_card(self, cards):
        '''
        剔除传入的牌
        :param cards:要剔除的牌的十六进制的表达
        '''
        for i in cards:
            self.poker_set_round.remove(i)

    @staticmethod
    def print_show(s):
        color = ["♢", "♣", "♡", "♠"]
        number = s & 0xf
        if number == 14 or number == 1:
            number = 'A'
        elif number == 11:
            number = 'J'
        elif number == 12:
            number = 'Q'
        elif number == 13:
            number = 'K'
        show = color[s >> 4] + str(number)
        print(show, end=" ")

    @staticmethod
    def switch_poker_number(number):
        result = str(number)
        if number == 14 or number == 1:
            result = 'A'
        elif number == 10:
            result = 'T'
        elif number == 11:
            result = 'J'
        elif number == 12:
            result = 'Q'
        elif number == 13:
            result = 'K'
        return result

    # 先按花色再按点数排序
    @staticmethod
    def my_sort_poker(poker):
        return sorted(sorted(poker), key=lambda color: color & 0xf)

    @staticmethod
    def get_poker_set():
        poker_set = []
        for i in range(0, 4):
            poker_set += [x | (0x10 * i) for x in [x for x in range(2, 15)]]
        return poker_set

        # type 0  straight flush   royal flush　同花顺
        # 1 four of a kind　四带一
        # 2 full house　三带二
        # 3 flush　同花
        # 4 straight　顺子
        # 5 three of a kind　三条
        # 6 two pairs　两对
        # 7  one pairs　一对
        # 8 hard card　高牌

    @staticmethod
    def jugg_type(input_poker):
        p_type = 8
        key = []

        my_poker = Poker.my_sort_poker(input_poker)
        most_color = Counter([x >> 4 for x in my_poker]).most_common()[0]  # 花色数的统计,取最大数
        if most_color[1] > 4:  # 有五张同花 此处在找同花，还有同花顺，对应类型 3 0
            some_color_p = [x & 0xf for x in list(filter(lambda x: x >> 4 == most_color[0], my_poker))]
            p_type = 3  # flush
            key.clear()
            key += list(reversed(some_color_p))[0:5]
            # 不返回是因为后面还可能有更大的
            # return p_type, key
            result = Poker.straight(some_color_p)
            if result is not None:
                p_type = 0  # straight flush
                key.clear()
                key += result[1]
                return p_type, key

        poker_no_color = [x & 0xf for x in my_poker]
        number_count = Counter(poker_no_color).most_common()

        if len(number_count) >= 5 and p_type > 4:  # 找顺子，对应类型 4　此之前最多被同花给覆盖
            result = Poker.straight(sorted([x[0] for x in number_count]))
            if result is not None:
                p_type = 4  # straight
                key.clear()
                key += result[1]
                # 不返回是因为后面还可能有更大的
                # return p_type, key

        # 同一点数数量最多的
        if number_count[0][1] == 4:  # four of kind
            p_type = 1
            key.clear()
            key.append(number_count[0][0])  # 四
            del number_count[0]  # 删除四条
            key.append(sorted(number_count, reverse=True)[0][0])  # 一
            return p_type, key
        # 有三条
        if number_count[0][1] == 3:
            three = sorted([x for x in number_count if x[1] == 3], reverse=True)
            if len(three) == 2:  # double three full house　两副三条
                p_type = 2
                key.clear()
                key.append(three[0][0])  # 三
                key.append(three[1][0])  # 对
                return p_type, key

            pairs = sorted([x for x in number_count if x[1] == 2], reverse=True)
            if len(pairs) > 0:  # full house
                p_type = 2
                key.clear()
                key.append(three[0][0])  # 三
                key.append(pairs[0][0])  # 对
                return p_type, key
            if p_type > 4:  # three of a kind
                p_type = 5
                key.clear()
                key.append(three[0][0])  # 三
                number_count.remove(three[0])  # 删除三条
                high_card = [x[0] for x in sorted(number_count, reverse=True)]
                key.append(high_card[0:2])
                return p_type, key
        # 找有对
        if number_count[0][1] == 2 and p_type > 4:
            pairs = sorted([x for x in number_count if x[1] == 2], reverse=True)
            if len(pairs) >= 2:
                p_type = 6
                key.clear()
                key.append(pairs[0][0])  # 两对
                key.append(pairs[1][0])
                number_count.remove(pairs[0])  # 删除已增加的对
                number_count.remove(pairs[1])  # 删除已增加的对
                high_card = [x[0] for x in sorted(number_count, reverse=True)]
                key.append(high_card[0])
                return p_type, key
            if len(pairs) == 1:
                p_type = 7
                key.clear()
                key.append(pairs[0][0])  # 一对
                number_count.remove(pairs[0])  # 删除已增加的对
                high_card = [x[0] for x in sorted(number_count, reverse=True)]
                key.append(high_card[0:3])
                return p_type, key

        if p_type == 8:
            poker_no_color.reverse()
            key = poker_no_color[0:5]
        return p_type, key

    @staticmethod
    def straight(poker):
        if len(poker) >= 5:
            s = 1
            for i in range(len(poker) - 2, -1, -1):
                if poker[i] + 1 == poker[i + 1]:
                    s += 1
                else:
                    s = 1
                if s == 5:
                    return True, list(reversed(poker[i:i + 5]))
            # 特殊的A2345情况 A2345<23456
            if 14 in poker:
                poker = [x if x != 14 else 1 for x in poker]
                poker.sort()
                s = 1
                for i in range(len(poker) - 2, -1, -1):
                    if poker[i] + 1 == poker[i + 1]:
                        s += 1
                    else:
                        s = 1
                    if s == 5:
                        return True, list(reversed(poker[i:i + 5]))

    @staticmethod
    def get_poker_from_string(s):
        poker_set = []
        base = 0
        for i in s:
            p = "dchs".find(i)  # 方块　梅花　红心　黑桃
            if p == -1:  # 为数字
                p = "TJQKA".find(i)
                if p == -1:
                    base = int(i)
                else:
                    base = p + 10
            else:
                poker_set.append(base | (0x10 * p))

        return poker_set

    def get_poker_all_color(self, n):
        '''
        从单数取全部花色的字符串
        :param n: 可为数字可为字符串
        :return: 全花色数组的数字
        '''
        return self.get_poker_from_string(''.join([f'{n}{x}' for x in 'dchs']))

    def get_poker_plus_to(self, start, end):
        order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        s = order.index(start) + 2
        e = order.index(end) + 2
        r = []
        for i in range(s, e + 1):
            r.append(self.switch_poker_number(i))
        return r
