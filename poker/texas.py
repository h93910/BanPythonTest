from .texas_bot import TexasHoldemPokerBOT
from .poker import Poker
import random
import time


class TexasHoldemPoker:
    def __init__(self, bankroll_list: list):
        self.bankroll = bankroll_list
        self.tool = Poker()
        self.BB = 200

        self.pool = None
        self.sb_position = None
        self.on_play = None
        self.public = None
        self.player = None
        self.bots = None
        self.human = None
        self.cheat = True
        pass

    def start_round(self, sb_position, have_human):
        self.pool = [0] * len(self.bankroll)
        self.sb_position = sb_position
        self.on_play = [True] * len(self.bankroll)
        self.public = []
        self.player = []
        self.bots = []
        self.human = have_human

        print("==========new round============")
        # print money
        for i in range(len(self.bankroll)):
            print("%s:%d" % (self.bankroll[i][0], self.bankroll[i][1]), end=" ")
            if "bot" in self.bankroll[i][0]:
                self.bots.append(TexasHoldemPokerBOT())
            else:
                self.bots.append(None)
            if self.bankroll[i][1] == 0:
                self.on_play[i] = False
        print()
        self.pre_flop()
        if self.check_end(False):
            return
        self.flop()
        if self.check_end(False):
            return
        self.turn()
        if self.check_end(False):
            return
        self.river()
        self.check_end(True)

    def pre_flop(self):
        self.tool.init_poker()
        print("\npre-flops")
        # pre-flops show
        for i in range(len(self.bankroll)):
            if self.bankroll[i][1] != 0:
                self.player.append(self.tool.get_card(2))
                if not self.human:
                    print(self.bankroll[i][0], end=" ")
                    self.print_public(self.player[i])
            else:
                self.player.append(None)
                print("%s out" % self.bankroll[i][0])

        # bet for blind
        single_pool = [0] * len(self.bankroll)

        for i in range(len(self.bankroll)):
            position = (i + self.sb_position) % len(self.bankroll)
            if i == 0:
                single_pool[position] = self.BB / 2 if self.bankroll[position][1] > (self.BB / 2) else \
                    self.bankroll[position][1]
                print("%s:SB" % self.bankroll[position][0], end=" ")
            else:
                while self.on_play[position] is False:  # 已出局
                    position = (position + 1) % len(self.bankroll)
                single_pool[position] = self.BB if self.bankroll[position][1] > self.BB else self.bankroll[position][1]
                print("%s:BB" % self.bankroll[position][0])
                break

        # BB next guy
        bet_position = (position + 1) % len(self.bankroll)
        while self.on_play[bet_position] is False:
            bet_position = (bet_position + 1) % len(self.bankroll)
        self.bet(bet_position, single_pool)

    def flop(self):
        # show flop
        print("\nflop:", end="")
        self.public += self.tool.get_card(3)
        self.print_public(self.public)

        temp = []
        for i in range(len(self.on_play)):
            if self.on_play[i]:
                temp.append(self.bankroll[i][1])
        if len([x for x in temp if x != 0]) >= 2:  # 大于两人
            self.bet(self.sb_position, [0] * len(self.bankroll))

    def turn(self):
        # show turn
        print("\nturn:", end="")
        self.public += self.tool.get_card(1)
        self.print_public(self.public)

        temp = []
        for i in range(len(self.on_play)):
            if self.on_play[i]:
                temp.append(self.bankroll[i][1])
        if len([x for x in temp if x != 0]) >= 2:  # 大于两人
            self.bet(self.sb_position, [0] * len(self.bankroll))

    def river(self):
        # show river
        print("\nriver:", end="")
        self.public += self.tool.get_card(1)
        self.print_public(self.public)

        temp = []
        for i in range(len(self.on_play)):
            if self.on_play[i]:
                temp.append(self.bankroll[i][1])
        if len([x for x in temp if x != 0]) >= 2:  # 大于两人
            self.bet(self.sb_position, [0] * len(self.bankroll))

    def bet(self, bet_position, single_pool):
        i = 0
        while i != len(self.bankroll):
            position = (i + bet_position) % len(self.bankroll)
            if self.on_play[position] is False or self.bankroll[position][1] == single_pool[position] or \
                            self.bankroll[position][1] == 0:  # remove fold player or 0 money player
                i += 1
                continue
            if len([x for x in self.on_play if x]) == 1:  # only one man left, dont need to continue now
                break
            base_money = max(single_pool)
            reset = False
            while True:
                if self.on_play[position] and self.bankroll[position][0] == 0:
                    break

                if "bot" in self.bankroll[position][0]:
                    human_on = False
                    for j in range(len(self.on_play)):
                        if "bot" not in self.bankroll[j][0] and self.on_play[j]:
                            human_on = True
                            break
                    if human_on:
                        time.sleep(1)

                    if "bot_p" in self.bankroll[position][0]:
                        operation = self.bots[position].thinking_primary(
                            self.bankroll[position][1], single_pool[position] == base_money, self.BB,
                            self.public, self.player[position], len([x for x in self.on_play if x]) - 1,
                            self.pool, single_pool, self.human)
                    else:
                        operation = self.bots[position].thinking_random(
                            self.bankroll[position][1], single_pool[position] == base_money, self.BB)
                    print("%s operation:%s" % (self.bankroll[position][0], operation))
                else:
                    if self.cheat:
                        print("============\n", self.bankroll[position][0], "  ",
                              TexasHoldemPokerBOT.win(self.public, self.player[position],
                                                      len([x for x in self.on_play if x]) - 1), end=" ")
                    else:
                        print("============\n", self.bankroll[position][0], end=" ")
                    self.print_public(self.player[position])
                    operation = input("%s plz make u operation:" % self.bankroll[position][0])

                if self.bankroll[position][1] < base_money and "raise:" in operation:
                    print("Do u want to raise ? but u money is low,so raise become to all in")
                    operation = "all in"
                if "check" in operation:
                    if single_pool[position] == base_money:
                        break
                    else:
                        print("""u can't check,only fold or flat or raise""")
                elif "fold" in operation:
                    self.on_play[position] = False
                    if "show me" in operation:
                        for j in range(len(self.player)):
                            print(self.bankroll[j][0], end=" ")
                            self.print_public(self.player[j])
                    break
                elif "flat" in operation:
                    if single_pool[position] <= base_money:
                        single_pool[position] = base_money if self.bankroll[position][1] >= base_money else \
                            self.bankroll[position][1]
                        break
                elif "all in" in operation:
                    single_pool[position] = self.bankroll[position][1]
                    if single_pool[position] > base_money:
                        bet_position = position
                        reset = True
                    break
                elif "raise:" in operation:
                    r = int(operation.split(":")[1])
                    if r > self.bankroll[position][1] - single_pool[position]:
                        print("u only can bet:%d" % (self.bankroll[position][1] - single_pool[position]))
                    elif r + single_pool[position] < base_money:
                        print("too low,it must >%d" % (base_money - single_pool[position]))
                    elif r % 10 != 0:
                        print("raise must be multiple of 10")
                    else:
                        single_pool[position] += r
                        bet_position = position
                        reset = True
                        break
                else:
                    print("unknown operation")
            if reset:
                i = 1
            else:
                i += 1
        # 结算
        for i in range(len(single_pool)):
            self.bankroll[i][1] -= single_pool[i]
            self.pool[i] += single_pool[i]

    def check_end(self, end):
        if len([x for x in self.on_play if x]) == 1:
            for i in range(len(self.on_play)):
                if self.on_play[i]:
                    print("winner:%s" % self.bankroll[i][0])
                    self.bankroll[i][1] += sum(self.pool)
                    return True
        if end:  # river pk
            my_round = 1
            while len([x for x in self.on_play if x]) >= 2:
                bonus = min([x for x in self.pool if x != 0])
                print("\nround%d , base bonus:%d" % (my_round, bonus))
                pk_set = []
                for i in range(len(self.on_play)):
                    if self.on_play[i]:
                        player_combination = Poker.jugg_type(self.public.copy() + list(self.player[i]))
                        print("%s:%s" % (self.bankroll[i][0], self.card_type(player_combination)))
                        pk_set.append(player_combination)
                    else:
                        pk_set.append((99, 0))
                pk_result_set = sorted(pk_set, key=lambda x: (-x[0], x[1]))
                max_p = pk_result_set[-1]
                print("max:%s" % self.card_type(max_p))
                winners = []
                for i in range(len(pk_set)):
                    if pk_set[i] == max_p:
                        winners.append(i)
                winner_bonus = bonus * len([x for x in self.pool if x != 0]) / len(winners)
                for i in winners:
                    print("winner:%s" % self.bankroll[i][0])
                    self.bankroll[i][1] += winner_bonus
                for i in range(len(self.pool)):
                    if self.pool[i] != 0:
                        self.pool[i] -= bonus
                for i in range(len(self.pool)):
                    if self.pool[i] == 0:
                        self.on_play[i] = False
                my_round += 1
            else:
                if len([x for x in self.on_play if x]) == 1:
                    for i in range(len(self.on_play)):
                        if self.on_play[i]:
                            print(
                                "\nround%d , left bonus:%d all to %s" % (my_round, sum(self.pool), self.bankroll[i][0]))
                            self.bankroll[i][1] += sum(self.pool)

        return False

    def deal_operation(self):
        pass

    def print_public(self, p):
        for i in p:
            self.tool.print_show(i)
        print()

    # -1为左右赢 0为平手 1为右边赢
    def pk(self, set):
        result = Poker.jugg_type(set[0])
        result2 = Poker.jugg_type(set[1])

        if result[0] < result2[0]:
            win = -1
        elif result[0] == result2[0]:
            if result == result2:
                win = 0
            elif result[1] > result2[1]:
                win = -1
            else:
                win = 1
        else:
            win = 1

        if win != 1:
            return win
        print("A:", end="")
        for i in set[0]:
            self.tool.print_show(i)
        print(result, end=" ")
        print(" " + self.card_type(result) + " " + ("win" if win == -1 else "") + ("draw" if win == 0 else""))

        print("B:", end="")
        for i in set[1]:
            self.tool.print_show(i)
        print(result2, end=" ")
        print(" " + self.card_type(result2) + " " + ("win" if win == 1 else "") + ("draw" if win == 0 else""))

        print()

        return win

    def card_type(self, result):
        s = ""
        if result[0] == 0:
            s = "straight flush:high "
            for i in result[1]:
                s += self.tool.switch_poker_number(i)
        elif result[0] == 1:
            s = "four of a kind: " + self.tool.switch_poker_number(result[1][0]) * 4 + self.tool.switch_poker_number(
                result[1][1])
        elif result[0] == 2:
            s = "full house: " + self.tool.switch_poker_number(result[1][0]) * 3 + " " + self.tool.switch_poker_number(
                result[1][1]) * 2
        elif result[0] == 3:
            s = "flush:high "
            for i in result[1]:
                s += self.tool.switch_poker_number(i)
        elif result[0] == 4:
            s = "straight:high "
            for i in result[1]:
                s += self.tool.switch_poker_number(i)
        elif result[0] == 5:
            s = "three of a kind:" + self.tool.switch_poker_number(result[1][0]) * 3 + " high:"
            for i in result[1][1]:
                s += self.tool.switch_poker_number(i)
        elif result[0] == 6:
            s = "two pairs: " + self.tool.switch_poker_number(result[1][0]) * 2 + " " + self.tool.switch_poker_number(
                result[1][1]) * 2 + " high:" + self.tool.switch_poker_number(result[1][2])
        elif result[0] == 7:
            s = "one pairs: " + self.tool.switch_poker_number(result[1][0]) * 2 + " high:"
            for i in result[1][1]:
                s += self.tool.switch_poker_number(i)
        elif result[0] == 8:
            s = "hard card:"
            for i in result[1]:
                s += self.tool.switch_poker_number(i)
        return s

    def test(self):
        p = []
        for i in range(0, 4):
            p += [x | (0x10 * i) for x in [x for x in range(2, 15)]]

        p2 = p.copy()
        # pokerii = []
        # for i in range(7):
        #     r = random.randint(0, len(p2) - 1)
        #     pokerii.append(p2[r])
        #     del p2[r]
        # pokerii = [0x2, 0x3, 0x4, 0x5, 0x6, 0x23, 0x2A]
        # print(self.card_type(Poker.jugg_type(pokerii)))

        # for i in sorted(pokerii):
        # for i in self.my_sort_poker(pokerii):
        #     self.print_show(i)
        # print()

        public = []
        for i in range(5):
            r = random.randint(0, len(p2) - 1)
            public.append(p2[r])
            del p2[r]

        A = public.copy()
        B = public.copy()
        for i in range(2):
            r = random.randint(0, len(p2) - 1)
            A.append(p2[r])
            del p2[r]

        for i in range(2):
            r = random.randint(0, len(p2) - 1)
            B.append(p2[r])
            del p2[r]

        return self.pk((A, B))


        # p2 = p.copy()
        # one = []
        # two = []
        # three = []
        # for j in range(3):
        #     for i in range(1, 18):
        #         r = random.randint(0, len(p2) - 1)
        #         if j == 0:
        #             one.append(p2[r])
        #         elif j == 1:
        #             two.append(p2[r])
        #         elif j == 2:
        #             three.append(p2[r])
        #         del p2[r]
        #
        # for i in my_sort_poker(one):
        #     print_show(i)
        # print()
        #
        # for i in my_sort_poker(two):
        #     print_show(i)
        # print()
        #
        # for i in my_sort_poker(three):
        #     print_show(i)
        # print()
