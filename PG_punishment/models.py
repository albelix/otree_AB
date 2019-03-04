from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
# from tables import group

# import random

from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.db import models
# from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

author = 'Alexis Belianin'

doc = """
PG game with punishment 
"""


class Constants(BaseConstants):
    name_in_url = 'PG_punishment'
    players_per_group = 7
    num_rounds = 8
    endowment = c(100)
    lumpsum = c(160)
    efficiency_factor = 2
    contribution_limits = currency_range(0, endowment, 1)  # define range of contribs
    num_decisions_per_round = 2
    pun_endowment = 40  # max amount spent on punishment
    pun_factor = 2  # efficiency of punishment


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_pgg_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.pgg_payoff = Constants.endowment - p.contribution + self.individual_share


class Player(BasePlayer):
    contribution = models.CurrencyField(doc="""The amount contributed by the player""", min=0, max=100, )
    pgg_payoff = models.CurrencyField(doc='to store intermediary profit from pgg before punishment stage', initial=0)
    punishment_sent = models.CurrencyField(doc='amount of deduction tokens sent', min=0, max=Constants.pun_endowment)
    punishment_received = models.CurrencyField(doc='amount of pun received multiplied by factor', min=0)
    retained_income = models.CurrencyField(doc='retained part of endowment', min=0)
    cumulative_intermediate_profit = models.CurrencyField(doc='profit accumulated before punishment', min=0)

    def set_punishment_received(self):
        all_puns_received = [getattr(i, 'pun_{}'.format(self.id_in_group)) for i in self.get_others_in_group()]
        self.punishment_received = sum(all_puns_received) * Constants.pun_factor

    def set_punishment_sent(self):
        all_puns_sent = [getattr(self, 'pun_{}'.format(i.id_in_group)) for i in self.get_others_in_group()]
        self.punishment_sent = sum(all_puns_sent)

    def set_pun(self):
        self.set_punishment_sent()
        self.set_punishment_received()

    def set_final_payoff(self):
        self.payoff = Constants.endowment - self.contribution + self.pgg_payoff - (self.punishment_sent + self.punishment_received)

    def retain_income(self):
        self.retained_income = Constants.endowment - self.contribution
        # return{
        #     'retained_income': Constants.endowment - self.contribution
        # }

    def my_method(self):
        self.my_contribution = sum([p.contribution for p in self.in_all_rounds()])
        self.my_payoff = sum([p.payoff for p in self.in_all_rounds()]) + self.retained_income
        # return{
        #     'cumulative_intermediate_income': sum([p.payoff for p in self.in_all_rounds()]) + self.retained_income
        # }




for i in range(1, Constants.players_per_group + 1):
    Player.add_to_class('pun_{}'.format(i),
                        models.CurrencyField(min=0,
                                             max=Constants.pun_endowment,
                                             verbose_name="Вычет у участника {}".format(i)))
