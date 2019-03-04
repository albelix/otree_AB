from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import random, randint

author = 'Alexis Belianin'

doc = """
PG game for EDots
"""

class Constants(BaseConstants):
    name_in_url = 'PG_threshold'
    players_per_group = 8
    num_rounds = 8
    endowment = c(100)
    lumpsum = c(160)
    threshold = c(3000) #c(2400)
    efficiency_factor = 2
    contribution_limits = currency_range(0, endowment, 1) #define range of contribs


class Subsession(BaseSubsession):
    flood = models.FloatField()
    def creating_session(self):
        for p in self.get_players():
            Group.flood = randint(1, Constants.threshold)/Constants.threshold

    def vars_for_admin_report(self):
        rollingshares = sorted([p.current_share for p in self.group.set_payoffs()])
        return {'rollingshares': rollingshares}

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    round_num=models.IntegerField()
    current_share=models.FloatField()
    # p1 = models.IntegerField()
    # p2 = models.IntegerField()
    # p3 = models.IntegerField()
    # p1_payoff = models.CurrencyField()
    # p2_payoff = models.CurrencyField()
    # p3_payoff = models.CurrencyField()
    global_contribution=models.CurrencyField()
    success=models.BooleanField()
    # glob_cont=models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        self.global_contribution = sum([p.total_contribution for p in self.in_all_rounds()])
        self.current_share=self.global_contribution*100 / Constants.threshold
        # if Group.flood<self.current_share:
        #     self.success = 1
        # else:
        #     self.success = 0

        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution # + self.individual_share
            # p1 = self.get_player_by_id(1)
            # p2 = self.get_player_by_id(2)
            # p3 = self.get_player_by_id(3)
            # p1_payoff = sum([p.payoff for p in self.in_previous_rounds() if p.p1 == 1])
            # p2_payoff = sum([p.payoff for p in self.in_previous_rounds() if p.p2 == 2])
            # p3_payoff = sum([p.payoff for p in self.in_previous_rounds() if p.p3 == 3])  # in_all_rounds
            print('p.payoff_is', p.payoff)

    # def globcont(self):
    #     self.glob_contribution = sum([p.total_contribution for p in self.in_all_rounds()])
    #     for p in self.in_all_rounds():
    #         p.glob_cont = self.glob_contribution
    #         print('*******my_payoff is', p.globcont)

    # def set_payoffs_all(self):
    #     p1 = self.get_player_by_id(1)
    #     p2 = self.get_player_by_id(2)
    #     p3 = self.get_player_by_id(3)
    #     print('*******p1 is', self.p1)
    #     print('*******p2 is', self.p2)
    #     print('*******p3 is', self.p3)
    #     # p4 = self.get_player_by_id(4)
    #     # p5 = self.get_player_by_id(5)
    #     p1_payoff = sum([p.payoff for p in self.in_previous_rounds() if self.p1 == 1])
    #     p2_payoff = sum([p.payoff for p in self.in_previous_rounds() if self.p2 == 2])
    #     p3_payoff = sum([p.payoff for p in self.in_previous_rounds() if self.p3 == 3]) # in_all_rounds
    #     print('*******p1_payoff is', self.p1_payoff)
    #     print('*******p2_payoff is', self.p2_payoff)
    #     print('*******p3_payoff is', self.p3_payoff)
        # p2.payoff = sum([p.payoff for p2 in self.in_all_rounds()])
        # p3.payoff = sum([p.payoff for p3 in self.in_all_rounds()])
        # p4.payoff = sum([p4.payoff for p4 in self.in_all_rounds()])
        # p5.payoff = sum([p5.payoff for p5 in self.in_all_rounds()])

    # def sum_in_previous_round(self):
    #     return sum(p.in_previous_rounds()[-1].payoff for p in self.get_players())

class Player(BasePlayer):
    contribution = models.CurrencyField(doc="""The amount contributed by the player""", min=0,max=100)
    payoff = models.CurrencyField()
    total_contribution = models.CurrencyField()
    my_contribution = models.CurrencyField(doc="""The amount contributed by the player""", )
    my_payoff = models.CurrencyField()
    my_cut_payoff = models.CurrencyField()
    # prof = models.CurrencyField()
    # contr = models.CurrencyField()
    # par1 = models.IntegerField()
    # par2 = models.IntegerField()
    # par3 = models.IntegerField()

    def my_method(self):
        self.my_contribution = sum([p.contribution for p in self.in_all_rounds()])
        self.my_payoff = sum([p.payoff for p in self.in_all_rounds()])
        self.my_cut_payoff = self.my_payoff*0.25
        return self.subsession.round_number
        #        self.others_choice = self.get_others_in_group()[1].my_payoff
        # for p in self.in_all_rounds():
        #     p.prof = p.my_payoff
        #     print('*******my_payoff is', p.prof)
        #     p.contr = p.my_contribution
        #     print('*******my_payoff is', p.contr)

                # def role(self):
                #    if self.id_in_group == 1:
                #        self.idind = 1
                #        self.par1 = self.my_payoff(1)
                #    if self.id_in_group == 2:
                #        self.idind = 2
                #        self.par2 = self.my_payoff(2)
                #    if self.id_in_group == 3:
                #        self.idind = 3
                #        self.par3 = self.my_payoff(3)


                #def role(self):
    #    if self.id_in_group == 1:
    #        self.idind = 1
    #        self.par1 = self.my_payoff(1)
    #    if self.id_in_group == 2:
    #        self.idind = 2
    #        self.par2 = self.my_payoff(2)
    #    if self.id_in_group == 3:
    #        self.idind = 3
    #        self.par3 = self.my_payoff(3)
