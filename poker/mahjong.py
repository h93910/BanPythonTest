import random
import re
import numpy as np

debug = False


class Mahjong:
    def __init__(self):
        万 = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
        筒 = [str(x) for x in range(1, 10)]
        条 = ['⑴', '⑵', '⑶', '⑷', '⑸', '⑹', '⑺', '⑻', '⑼']
        字 = ['东', '南', '西', '北', '中', '发', '白']
        self.card_set = []
        self.discard_set = []
        self.hide_card = []  # 其它玩家的牌
        self.base = []
        self.card_show = [万, 筒, 条, 字]
        self.reset()

    def reset(self):
        """重置牌"""
        # 十进制,1~9万,11~19筒,21~29条,30~36东南西北中发白
        self.base = list(filter(lambda x: x >= 30 or x % 10 != 0, [x for x in range(1, 37)]))
        self.card_set = self.base * 4
        self.discard_set.clear()
        self.hide_card.clear()

    def get_show(self, number):
        c = ['\033[31m', '\033[34m', '\033[32m', '\033[36m']
        """显示牌"""
        t = number // 10  # 取除整法
        n = number % 10
        if t < 3:
            n -= 1  # 非字牌从1开始记数
        return c[t] + self.card_show[t][n]

    def get_cards(self, count, exclude=None):
        """
        发牌
        :param exclude: 排除的牌
        :param count: 发几张
        """
        cards = []
        for i in range(count):
            r = random.randint(0, len(self.card_set) - 1)
            if exclude is not None:
                while self.card_set[r] in exclude:
                    r = random.randint(0, len(self.card_set) - 1)
            cards.append(self.card_set[r])
            del self.card_set[r]
            # r = np.random.choice(self.card_set)
            # cards.append(r)
            # index = np.where(r == self.card_set)
            # self.card_set = np.delete(self.card_set, index[0].min())
        return cards

    def remove_cards(self, s):
        for i in s:
            self.card_set.remove(i)

    def discard_card(self, s):
        self.discard_set += s

    def print_show(self, cards, posistion=True):
        """
        打印牌
        :param cards: 手牌库
        print('\033[30m这是前景色0')
        30                40              黑色
        31                41              红色
        32                42              绿色
        33                43              黃色
        34                44              蓝色
        35                45              洋红
        36                46              青色
        37                47              白色
        """
        for i, element in enumerate(cards):
            if posistion:
                print("%s\033[0m(%d)" % (self.get_show(element), i + 1), end=' ')
            else:
                print(self.get_show(element), end=' ')
        print("\033[0m")

    def has_alphabet(self, s):
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, s)
        if len(res):
            return True
        else:
            return False

    def grouping_and_ramdom(self, book, bs, hs):
        """
        分组并进行位移
        :param book:
        :param bs:
        :param hs:
        :return:
        """

        book_slice = bs.copy()
        hu_slice = hs.copy()
        # 分割
        group_ascii = [[49, 57], [97, 103], [104, 110], [120, 122]]  # 1~9 a~g h~m x~z
        for i in group_ascii:
            b = list(filter(lambda x: ord(x) in range(i[0], i[1] + 1), book_slice))
            h = list(filter(lambda x: ord(x) in range(i[0], i[1] + 1), hu_slice))
            if len(b) != 0 and len(h) != 0:
                book.append({'book': b, 'hu': h, 'group': i})
        if debug:
            print(book)
        # 全转为数字
        for i in book:
            if i['group'] == group_ascii[3]:  # 随机牌不换
                continue
            i['book'] = list(map(lambda x: ord(x) - i['group'][0] + 1, i['book']))
            i['hu'] = list(map(lambda x: ord(x) - i['group'][0] + 1, i['hu']))
        # 随机位移
        for i in book:
            if i['group'] == group_ascii[3]:  # 随机牌不偏移
                continue
            if i['group'] == group_ascii[0] and min(i['book']) == 1 or max(i['book'] + i['hu']) == 9:  # 牌型为边张，不进行位移
                continue
            # 偏移等于分组最大张与牌型最大张之间的距离
            offset = random.randint(0, 9 - max(i['book'] + i['hu']))
            if offset != 0:
                i['book'] = list(map(lambda x: x + offset, i['book']))
                i['hu'] = list(map(lambda x: x + offset, i['hu']))
        # 转换成最终牌的值
        card_type = [0, 10, 20]
        for i in book:
            if i['group'] != group_ascii[3]:
                r = random.randint(0, len(card_type) - 1)
                t = card_type[r]
                del card_type[r]
                i['book'] = list(map(lambda x: x + t, i['book']))
                i['hu'] = list(map(lambda x: x + t, i['hu']))
            else:  # 随机牌
                s = np.unique(i['book'] + i['hu'])
                for z in s:
                    now_exist = sum(list(map(lambda x: x['book'] + x['hu'], book)), [])
                    random_card = np.random.choice(self.base)
                    while random_card in now_exist:
                        random_card = np.random.choice(self.base)
                    i['book'] = np.where(np.array(i['book']) == z, random_card, i['book']).tolist()
                    i['hu'] = np.where(np.array(i['hu']) == z, random_card, i['hu']).tolist()
                i['book'] = list(map(int, i['book']))
                i['hu'] = list(map(int, i['hu']))
        if debug:
            print(book)
            # while len(book_slice) != 0 or len(hu_slice) != 0:
            #     if len(book_slice) != 0:
            # chr()
            # ord()

    def real_train(self):
        self.reset()

        # 随机生成混淆牌
        hand = self.get_cards(13)
        self.hide_card += self.get_cards(13 * 3)  # 其它家
        # 模拟打牌过程
        turn = 0
        while len(self.card_set) > 0:
            turn += 1
            print('>%d巡 剩%d张' % (turn, len(self.card_set)))

            hand.sort()
            self.print_show(hand)

            draws = self.get_cards(4)
            draw = draws[0:1]
            self.discard_card(draws[1:4])
            while True:
                try:
                    ip = input("抓牌: %s\033[0m ,输入打出牌位置:" % self.get_show(draw[0]))
                    if ip == '':
                        p = -1
                    elif ip == 'check':
                        self.print_show(self.discard_set, posistion=False)
                        continue
                    else:
                        p = int(ip)
                    break
                except ValueError:
                    print('输入不合法，请重试')
            discard = draw
            if p == -1:
                self.discard_card(draw)
            elif p == 0:
                print("胡")
                hand += draw
                hand.sort()
                self.print_show(hand)
                break
            else:
                discard = [hand[p - 1]]
                self.discard_card(discard)
                del hand[p - 1]
                hand += draw
            print('打出了: ', end='')
            self.print_show(discard + draws[1:4], posistion=False)

    def train(self):
        self.reset()
        # 2开头为 2之后随机,xzy为随意牌,a开始为任意数字
        # 可加逆向
        spell_book = [
            # 五种听两张
            {'name': '两张-两面听', 'book': '23', 'hu': '14'},
            {'name': '两张-双碰听', 'book': 'xxyy', 'hu': 'xy'},
            {'name': '两张-双钓将', 'book': 'abcd', 'hu': 'ad'},
            {'name': '两张-单钓带边张', 'book': '1112', 'hu': '23'},
            {'name': '两张-单钓带嵌张', 'book': 'aaac', 'hu': 'bc'},
            # 八种听三张
            {'name': '三张-三面听', 'book': '23456', 'hu': '147'},
            {'name': '三张-三面钓将听', 'book': 'abcdefg', 'hu': 'adg'},
            {'name': '三张-单钓双碰听', 'book': 'aabbbcc', 'hu': 'abc'},
            {'name': '三张-单钓两面听', 'book': '2333', 'hu': '142'},
            {'name': '三张-双碰带嵌听', 'book': 'aaaccde', 'hu': 'bcf'},
            {'name': '三张-两面重双碰听', 'book': 'aaabcxx', 'hu': 'adx'},  # x如重叠记得特殊处理下
            {'name': '三张-双钓带嵌听', 'book': 'aaacdef', 'hu': 'bcf'},
            {'name': '三张-三碰听', 'book': 'aabbccddxx', 'hu': 'adx'},
            # 五种听四张
            {'name': '四张-四面听', 'book': '2344555', 'hu': '1436'},
            {'name': '四张-重三碰两面听', 'book': 'aaabbcc', 'hu': 'abcd'},
            {'name': '四张-双碰两面听', 'book': 'aaabchhhij', 'hu': 'ahdk'},
            {'name': '四张-重双碰三面听', 'book': '23456777xx', 'hu': '147x'},
            {'name': '四张-单钓三面听', 'book': '2333456', 'hu': '1472'},
            {'name': '四张-四碰听', 'book': 'aabbccddee', 'hu': 'abde'},
            # 三种听五张
            {'name': '五张-单钓四面听', 'book': '2223444', 'hu': '14253'},
            {'name': '五张-双钓三面听', 'book': '2223456', 'hu': '36147'},
            {'name': '五张-单钓四碰听', 'book': 'aabbccddeexxx', 'hu': 'abdex'},
            # 三种听六张
            {'name': '六张-两坎夹连张顺子', 'book': '2223444567', 'hu': '142538'},
            {'name': '六张-一副一坎七连顺', 'book': '2223456789', 'hu': '147369'},
            {'name': '六张-一副两坎两连顺', 'book': 'aaabbbcdef', 'hu': 'abcdfg'},
            # 三种听七张
            {'name': '七张-牌铺以“五”为中心（以下“四”“六”已用完，无）', 'book': '2344445666678', 'hu': '1235789'},
            {'name': '七张-“三”“七”摸完叫对称（以下“三”“七”已用完，无）', 'book': '2333345677778', 'hu': '1245689'},
            {'name': '七张-顺连三坎三钓将', 'book': 'aaabbbcccdefg', 'hu': 'acdgbeh'},
            # 三种听八张
            {'name': '八张-单缺“幺”“九”的等差数列', 'book': '2223456777', 'hu': '14725836'},
            {'name': '八张-调换暗坎的“八角灯”（以下“六”已用完，无）', 'book': '1112345666678', 'hu': '12345789'},
            {'name': '八张-出“尖”缺“尖”的八门听（以下“七”已用完，无；“尖”指“三”或“七”）', 'book': '2223456677778', 'hu': '12345689'},
            # 三种听九张
            {'name': '九张-天衣无缝“九莲宝灯”', 'book': '1112345678999', 'hu': '123456789'},
        ]
        # self.has_alphabet(spell_book[0]['book'])

        spell = np.random.choice(spell_book)
        # spell = {'name': '四张-重双碰三面听', 'book': '23456777xx', 'hu': '147x'}
        # 计算牌型与胡牌的可偏移
        book_slice = list(filter(lambda x: x != '', re.split('', spell['book'])))
        hu_slice = list(filter(lambda x: x != '', re.split('', spell['hu'])))
        ##　牌型分组
        book = []
        self.grouping_and_ramdom(book, book_slice, hu_slice)
        book_slice = sum(list(map(lambda x: x['book'], book)), [])
        hu_slice = sum(list(map(lambda x: x['hu'], book)), [])
        # 抽出模拟牌，模拟听牌位为min(floor(book.size/2),4)
        train_number = len(book_slice) - int(min(np.floor(len(book_slice) / 2), 4))
        hand = list(np.random.choice(book_slice, train_number, replace=False, p=None))
        train_cards = book_slice.copy()
        for i in hand:
            try:
                train_cards.remove(i)
            except ValueError as e:
                print(e)
        self.remove_cards(hand)
        # 随机生成混淆牌
        hand += self.get_cards(13 - len(hand), book_slice + hu_slice)
        # 模拟打牌过程
        turn = 0
        is_hu = False
        while len(train_cards) > 0:
            turn += 1
            print('>%d巡' % turn)

            hand.sort()
            self.print_show(hand)
            if random.random() < 0.5:
                draw = self.get_cards(1, train_cards)
            else:
                draw = list(np.random.choice(train_cards, 1))
                train_cards.remove(draw[0])
            while True:
                try:
                    ip = input("抓牌: %s\033[0m ,输入打出牌位置:" % self.get_show(draw[0]))
                    if ip == '':
                        p = -1
                    else:
                        p = int(ip)
                    break
                except ValueError:
                    print('输入不合法，请重试')
            discard = draw
            if p == -1:
                self.discard_card(draw)
            elif p == 0:
                print("胡")
                is_hu = True
                hand += draw
                hand.sort()
                self.print_show(hand)
                break
            else:
                discard = [hand[p - 1]]
                self.discard_card(discard)
                del hand[p - 1]
                hand += draw
            print('打出了: %s \033[0m' % self.get_show(discard[0]))

        book_slice.sort()
        hu_slice.sort()
        print("结束，训练牌型为:\033[45m", spell['name'], "\033[0m")
        print("应留:", end="")
        self.print_show(book_slice, posistion=False)
        print("听:", end="")
        self.print_show(hu_slice, posistion=False)

        if is_hu: return True
        for i in book_slice:
            try:
                hand.remove(i)
            except ValueError:
                return False
        return True


if __name__ == "__main__":
    m = Mahjong()
    train = True
    if train:
        t = 0
        win = 0
        for a in range(1, 100):
            t += 1
            print('========　第%d轮　直接回车打出抓到的牌;0为直接胡 ========' % a)
            if m.train():
                win += 1
            print('===== 胜率:%d/%d=%f ======' % (win, t, win / t))
    else:
        m.real_train()
