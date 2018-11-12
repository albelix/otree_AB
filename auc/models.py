from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import numpy
import random


author = 'Ansty'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'auc'
    players_per_group = None
    num_rounds = 10

    num_ss = 2
    num_bs = 2
    list_of_ss_id = [i for i in range(1, num_ss + 1)]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):



    def set_valuations(self):

        for pl in self.get_players():
            pl.valuation = round(numpy.random.uniform(low=0.0, high=10.0),2)


    ss_auc_val_str = models.StringField()
    bs_auc_val_str = models.StringField()

    ss_auc_id_str = models.StringField()
    bs_auc_id_str = models.StringField()

    ss_auc_ind = models.IntegerField() # 0 if no auc, 1 if there is at leas one auc
    bs_auc_ind = models.IntegerField()

    ss_part_id_str = models.StringField()
    bs_part_id_str = models.StringField()


    def valuation_announcement(self):

        self.ss_auc_val_str = ""
        self.bs_auc_val_str = ""
        self.ss_auc_id_str = ""
        self.bs_auc_id_str = ""



        for pl in self.get_players():
            if pl.role() == "Seller" and pl.subrole == "auctioneer":
                self.ss_auc_val_str += " "
                self.ss_auc_val_str += str(pl.valuation)
                self.ss_auc_id_str += " "
                self.ss_auc_id_str += str(pl.id_in_group)
            if pl.role() == "Buyer" and pl.subrole == "auctioneer":
                self.bs_auc_val_str += " "
                self.bs_auc_val_str += str(pl.valuation)
                self.bs_auc_id_str += " "
                self.bs_auc_id_str += str(pl.id_in_group)

        if len(self.ss_auc_val_str) == 0:
            self.ss_auc_ind = 0
        else:
            self.ss_auc_ind = 1

        if len(self.bs_auc_val_str) == 0:
            self.bs_auc_ind = 0
        else:
            self.bs_auc_ind = 1



        self.ss_part_id_str = ""
        self.bs_part_id_str = ""

        for pl in self.get_players():
            if pl.role() == "Seller" and pl.subrole == "participant":
                self.ss_part_id_str += " "
                self.ss_part_id_str += str(pl.id_in_group)
            if pl.role() == "Buyer" and pl.subrole == "participant":
                self.bs_part_id_str += " "
                self.bs_part_id_str += str(pl.id_in_group)






    def SPSB(self):

        ss_part_id_list = [int(s) for s in self.ss_part_id_str.split()]
        bs_part_id_list = [int(s) for s in self.bs_part_id_str.split()]

        buyers_winners = []
        sellers_winners = []

        for pl in self.get_players():

            if pl.role() == "Seller" and pl.subrole == "auctioneer":

                bids = [] # all bids made for this auc
                parts = [] # all participants, who made bids for this auc

                for b_part in bs_part_id_list:
                   if self.get_player_by_id(b_part).buyerchoice == pl.id_in_group:
                        bids.append(self.get_player_by_id(b_part).buyerbid)
                        parts.append(b_part)

                pl.first_bid = 0
                pl.second_bid = 0
                pl.winner_id = 0


                winners_positions = []
                winners_id = []

                copy_bids = bids

                if len(bids) >=2:
                    if max(copy_bids) >= pl.valuation:
                        pl.first_bid = max(copy_bids)
                        winners_positions = [i for i in range(len(copy_bids)) if copy_bids[i] == pl.first_bid]
                        winners_id = [parts[i] for i in winners_positions]
                        # pl.winner_id = bs_part_id_list[random.choice(winners_id)]
                        pl.winner_id = random.choice(winners_id)
                        copy_bids.remove(max(copy_bids))
                        if max(copy_bids) >= pl.valuation:
                            pl.second_bid = max(copy_bids)
                        else:
                            pl.second_bid = pl.valuation
                    else:
                        pl.first_bid = -1 # it means there is no auction here

                if len(bids) == 1:
                    if max(bids) >= pl.valuation:
                        pl.first_bid = max(bids)
                        pl.second_bid = pl.valuation
                        pl.winner_id = parts[0]
                    else:
                        pl.first_bid = -1

                if len(bids) == 0:
                    pl.first_bid = -1

                if pl.winner_id != 0:
                    buyers_winners.append(pl.winner_id)


                # set payoff

                if pl.first_bid == -1:
                    pl.payoff = 0
                    pl.auc_realised = False
                else:
                    pl.payoff = pl.second_bid - pl.valuation
                    pl.auc_realised = True

            if pl.role() == "Buyer" and pl.subrole == "auctioneer":

                bids = []
                parts = []

                for s_part in ss_part_id_list:
                    if self.get_player_by_id(s_part).sellerchoice == pl.id_in_group:
                        bids.append(self.get_player_by_id(s_part).sellerbid)
                        parts.append(s_part)

                pl.first_bid = 0
                pl.second_bid = 0
                pl.winner_id = 0

                if len(bids) >= 2:
                    if min(bids) <= pl.valuation:
                        pl.first_bid = min(bids)
                        winners_positions = [i for i in range(len(bids)) if bids[i] == pl.first_bid]
                        winners_id = [parts[i] for i in winners_positions]
                        # pl.winner_id = bs_part_id_list[random.choice(winners_id)]
                        pl.winner_id = random.choice(winners_id)
                        bids.remove(min(bids))
                        if min(bids) <= pl.valuation:
                            pl.second_bid = min(bids)
                        else:
                            pl.second_bid = pl.valuation
                    else:
                        pl.first_bid = -1

                if len(bids) == 1:
                    if min(bids) <= pl.valuation:
                        pl.first_bid = min(bids)
                        pl.second_bid = pl.valuation
                        pl.winner_id = parts[0]
                    else:
                        pl.first_bid = -1

                if len(bids) == 0:
                    pl.first_bid = -1

                if pl.winner_id != 0:
                    sellers_winners.append(pl.winner_id)

                # set payoff

                if pl.first_bid == -1:
                    pl.payoff = 0
                    pl.auc_realised = False
                else:
                    pl.payoff = pl.valuation - pl.second_bid
                    pl.auc_realised = True


        for pl in self.get_players():

            if pl.role() == "Buyer" and pl.subrole == "participant":

                if pl.id_in_group in buyers_winners:
                    pl.payoff = pl.valuation - self.get_player_by_id(pl.buyerchoice).second_bid # -\
                                # self.get_player_by_id(pl.buyerchoice).valuation
                    # pl.payoff = pl.valuation - self.get_player_by_id(pl.buyerchoice).payoff -\
                    #             self.get_player_by_id(pl.buyerchoice).valuation
                    pl.part_is_winner = True

                else:

                    pl.payoff = 0
                    pl.part_is_winner = False

            if pl.role() == "Seller" and pl.subrole == "participant":

                if pl.id_in_group in sellers_winners:
                    pl.payoff = self.get_player_by_id(pl.sellerchoice).second_bid  - pl.valuation
                                # +\ self.get_player_by_id(pl.sellerchoice).valuation
                    # pl.payoff = self.get_player_by_id(pl.sellerchoice).payoff +\
                    #             self.get_player_by_id(pl.sellerchoice).valuation - pl.valuation
                    pl.part_is_winner = True

                else:
                    pl.payoff = 0
                    pl.part_is_winner = False




class Player(BasePlayer):

    def role(self):
        if self.id_in_group in Constants.list_of_ss_id:
            return "Seller"
        else:
            return "Buyer"

    valuation = models.FloatField()

    subrole = models.StringField(choices=['auctioneer', 'participant'])

    sellerchoice = models.IntegerField(min=0.00)
    sellerbid = models.FloatField()


    buyerchoice = models.IntegerField(min=0.00)
    buyerbid = models.FloatField()

    first_bid = models.FloatField()
    second_bid = models.FloatField()

    winner_id = models.IntegerField()

    part_is_winner = models.BooleanField()
    auc_realised = models.BooleanField()

# added
    def my_method(self):
        self.my_payoff = sum([p.payoff for p in self.in_all_rounds()])