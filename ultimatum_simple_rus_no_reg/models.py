from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
from random import shuffle

author = 'Ann'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'U'
    players_per_group = 2
    num_rounds = 3
    unitcost = 3.5


    instructions_template = 'ultimatum_simple_rus_no_reg/Instructions.html'

    endowments_list = [60, 100, 120]
    ecu_to_rur = 5

    payoff_if_rejected = 0

class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            #define payment round
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            #regroup players: those (a half) who enter first are 1st players(S), others -- 2nd(R)
            matrix_to_get = self.get_group_matrix()
            matrix_to_set = []
            senders_list = []
            receivers_list =[]

            if len(matrix_to_get) % 2 == 0:
                for i in range(int(len(matrix_to_get)/2)):
                    for p in range(2):
                        senders_list.append(matrix_to_get[i][p])
                for i in range(int(len(matrix_to_get)/2), len(matrix_to_get)):
                    for p in range(2):
                        receivers_list.append(matrix_to_get[i][p])

                shuffle(senders_list)
                shuffle(receivers_list)

                for i in range(len(matrix_to_get)):
                    group = [senders_list[i], receivers_list[i]]
                    matrix_to_set.append(group)


                self.set_group_matrix(matrix_to_set)

            if len(matrix_to_get) % 2 != 0:
                for i in range(int((len(matrix_to_get) - 1) / 2)):
                    for p in range(2):
                        senders_list.append(matrix_to_get[i][p])

                i = int((len(matrix_to_get) - 1) / 2)
                senders_list.append(matrix_to_get[i][0])
                receivers_list.append(matrix_to_get[i][1])

                for i in range(int((len(matrix_to_get) + 1) / 2), len(matrix_to_get)):
                    for p in range(2):
                        receivers_list.append(matrix_to_get[i][p])

                shuffle(senders_list)
                shuffle(receivers_list)

                for i in range(len(matrix_to_get)):
                    group = [senders_list[i], receivers_list[i]]
                    matrix_to_set.append(group)

                self.set_group_matrix(matrix_to_set)

        else:
            self.group_like_round(1)




class Group(BaseGroup):

    # quiz

    S_quiz_1 = models.IntegerField()
    S_quiz_2 = models.IntegerField()
    S_quiz_3 = models.IntegerField()
    S_quiz_4 = models.IntegerField()
    S_quiz_5 = models.IntegerField()
    S_quiz_6 = models.IntegerField()
    S_quiz_7 = models.IntegerField()
    S_quiz_8 = models.IntegerField()

    R_quiz_1 = models.IntegerField()
    R_quiz_2 = models.IntegerField()
    R_quiz_3 = models.IntegerField()
    R_quiz_4 = models.IntegerField()
    R_quiz_5 = models.IntegerField()
    R_quiz_6 = models.IntegerField()
    R_quiz_7 = models.IntegerField()
    R_quiz_8 = models.IntegerField()

    # S answers

    S_transfer = models.IntegerField(min=0)
    S_self_part = models.IntegerField(min=0)

    S_prediction = models.IntegerField(min=0)


    # R answers

    R_min_acceptance = models.IntegerField(min=0)

    R_prediction = models.IntegerField(min=0)


    # set current payoffs (players don't observe these)

    S_payoff = models.IntegerField()
    R_payoff = models.IntegerField()

    def set_payoffs(self):
        if self.S_transfer >= self.R_min_acceptance:
            self.S_payoff = Constants.endowments_list[self.round_number - 1] - self.S_transfer
            self.R_payoff = self.S_transfer
        else:
            self.S_payoff = Constants.payoff_if_rejected
            self.R_payoff = Constants.payoff_if_rejected

    S_prediction_payoff = models.FloatField()
    R_prediction_payoff = models.FloatField()

    def prediction_payoffs(self):
        self.S_prediction_payoff = round((Constants.endowments_list[self.round_number - 1]/2) * (1 - abs((self.S_prediction - self.R_min_acceptance)/Constants.endowments_list[self.round_number - 1])),2)
        self.R_prediction_payoff = round((Constants.endowments_list[self.round_number - 1]/2) * (1 - abs((self.R_prediction - self.S_transfer)/Constants.endowments_list[self.round_number - 1])),2)


    # set paying round attributes

    paying_round_num = models.IntegerField()
    pie_size_final = models.IntegerField()

    S_prediction_final = models.IntegerField()
    R_min_acceptance_final = models.IntegerField()
    R_prediction_final = models.IntegerField()
    S_transfer_final = models.IntegerField()

    def set_paying_round_attributes(self):

        self.paying_round_num = self.session.vars['paying_round']

        self.pie_size_final = Constants.endowments_list[self.paying_round_num-1]

        if self.round_number < self.paying_round_num:
            self.S_prediction_final = 0
            self.R_min_acceptance_final = 0
            self.R_prediction_final = 0
            self.S_transfer_final = 0
        elif self.round_number >= self.paying_round_num:
            self.S_prediction_final = self.in_round(self.paying_round_num).S_prediction
            self.R_min_acceptance_final = self.in_round(self.paying_round_num).R_min_acceptance
            self.R_prediction_final = self.in_round(self.paying_round_num).R_prediction
            self.S_transfer_final = self.in_round(self.paying_round_num).S_transfer



    # set final payoffs

    S_final_payoff = models.IntegerField()
    R_final_payoff = models.IntegerField()
    S_final_prediction_payoff = models.FloatField()
    R_final_prediction_payoff = models.FloatField()
    S_total_payoff = models.FloatField()
    R_total_payoff = models.FloatField()

    def set_final_payoffs(self):
        if self.round_number < self.paying_round_num:
            self.S_final_payoff = 0
            self.R_final_payoff = 0
            self.S_final_prediction_payoff = 0
            self.R_final_prediction_payoff = 0
        else:
            self.S_final_payoff = self.in_round(self.paying_round_num).S_payoff
            self.R_final_payoff = self.in_round(self.paying_round_num).R_payoff
            self.S_final_prediction_payoff = self.in_round(self.paying_round_num).S_prediction_payoff
            self.R_final_prediction_payoff = self.in_round(self.paying_round_num).R_prediction_payoff
            self.S_total_payoff = self.S_final_payoff + self.S_final_prediction_payoff
            self.R_total_payoff = self.R_final_payoff + self.R_final_prediction_payoff

    # set final payoffs in rub

    def set_payoffs_in_rub(self):
        if self.round_number < self.paying_round_num:
            for p in self.get_players():
                p.payoff = c(0)

        if self.round_number >= self.paying_round_num:
            p1, p2 = self.get_players()[0], self.get_players()[1]
            p1.payoff = c((self.S_final_payoff + self.S_final_prediction_payoff)*Constants.unitcost) + c(150)
            p2.payoff = c((self.R_final_payoff + self.R_final_prediction_payoff)*Constants.unitcost) + c(150)


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'Sender'
        else:
            return 'Receiver'