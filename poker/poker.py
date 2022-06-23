import random


class Poker:
    def __init__(self):
        self.poker_set = []
        for i in range(0, 4):
            self.poker_set += [x | (0x10 * i) for x in [x for x in range(2, 15)]]

    def init_poker(self):
        self.poker_set_round = self.poker_set.copy()

    def get_card(self, count):
        card = []
        for i in range(count):
            r = random.randint(0, len(self.poker_set_round) - 1)
            card.append(self.poker_set_round[r])
            del self.poker_set_round[r]
        return card

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

        # type 0  straight flush   royal flush
        # 1 four of a kind
        # 2 full house
        # 3 flush
        # 4 straight
        # 5 three of a kind
        # 6 two pairs
        # 7  one pairs
        # 8 hard card

    @staticmethod
    def jugg_type(input_poker):
        p_type = 8
        key = []

        my_poker = Poker.my_sort_poker(input_poker)
        for i in range(4):
            some_color_p = [x & 0xf for x in list(filter(lambda x: x >> 4 == i, my_poker))]
            if len(some_color_p) >= 5:
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
        same_poker = dict()
        for i in poker_no_color:
            if i not in same_poker.keys():
                same_poker[i] = 1
            else:
                same_poker[i] += 1

        number_and_count = dict(sorted(same_poker.items(), key=lambda d: d[1], reverse=True))
        if len(number_and_count) >= 5:
            result = Poker.straight(sorted(list(number_and_count.keys()).copy()))
            if result is not None:
                if p_type > 4:
                    p_type = 4  # straight
                    key.clear()
                    key += result[1]
                    # 不返回是因为后面还可能有更大的
                    # return p_type, key

        for i in number_and_count:
            same_key_count = number_and_count[i]
            if same_key_count == 4:  # four of kind
                p_type = 1
                key.clear()
                key.append(i)  # 四
                del number_and_count[i]  # 删除四条
                key.append(sorted(number_and_count, reverse=True)[0])  # 一
                return p_type, key
            if same_key_count == 3:
                # 找对
                three = sorted(list(filter(lambda x: x[1] == 3, number_and_count.items())), reverse=True)
                if len(three) == 2:  # double three full house
                    p_type = 2
                    key.clear()
                    key.append(three[0][0])  # 三
                    key.append(three[1][0])  # 对
                    return p_type, key

                pairs = sorted(list(filter(lambda x: x[1] == 2, number_and_count.items())), reverse=True)
                if len(pairs) > 0:  # full house
                    p_type = 2
                    key.clear()
                    key.append(i)  # 三
                    key.append(pairs[0][0])  # 对
                    return p_type, key
                if p_type > 5:  # three of a kind
                    p_type = 5
                    key.clear()
                    key.append(i)  # 三
                    high_card = sorted(list(filter(lambda x: x != i, poker_no_color)), reverse=True)
                    key.append(high_card[0:2])
                    return p_type, key
            if same_key_count == 2:
                if p_type <= 5:
                    break
                # 找对
                pairs = sorted(list(filter(lambda x: x[1] == 2, number_and_count.items())), reverse=True)
                if len(pairs) >= 2:
                    p_type = 6
                    key.clear()
                    key.append(pairs[0][0])  # 两对
                    key.append(pairs[1][0])
                    high_card = sorted(
                        list(filter(lambda x: x != pairs[0][0] and x != pairs[1][0], poker_no_color)), reverse=True)
                    key.append(high_card[0])
                    return p_type, key
                if len(pairs) == 1:
                    p_type = 7
                    key.clear()
                    key.append(pairs[0][0])  # 一对
                    high_card = sorted(list(filter(lambda x: x != pairs[0][0], poker_no_color)), reverse=True)
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
        plus = 0
        for i in s.upper():
            p = "DCHS".find(i)
            if p == -1:  # 为数字
                p = "TJQKA".find(i)
                if p == -1:
                    p = int(i)
                else:
                    p += 10
                poker_set.append(p | (0x10 * plus))
            else:
                plus = p

        return poker_set
