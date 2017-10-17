import time

from bantest.poker.texas import TexasHoldemPoker
from bantest.poker.texas_bot import TexasHoldemPokerBOT

if __name__ == "__main__":
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