from poker import Poker
import random


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

    def C(self, n, m):
        level = lambda x: 1 if x == 1 else x * level(x - 1)
        first = level(n)
        second = level(m)
        third = level((n - m))
        return first // (second * third)
