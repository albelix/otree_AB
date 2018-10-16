from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from random import shuffle
import math



class Constants(BaseConstants):
    name_in_url = 'T'
    players_per_group = 2
    num_rounds = 3

    instructions_template = 'trust_rus_no_reg/Instructions.html'

    endowments_list = [100, 50, 100]
    factors_list = [3, 3, 1.5]
    ecu_to_rur = 5 #should be changed if an another region !!!!!!
    participation_payoff = c(150) #should be changed if an another region !!!!!!

    predictions_offer_r1 = [10,20,30,40,50,60,70,80,90,100]
    predictions_return_r1 = [30,60,90,120,150,180,210,240,270,300]

    predictions_offer_r2 = [5,10,15,20,25,30,35,40,45,50]
    predictions_return_r2 = [15,30,45,60,75,90,105,120,135,150]

    predictions_offer_r3 = [10,20,30,40,50,60,70,80,90,100]
    predictions_return_r3 = [15,30,45,60,75,90,105,120,135,150]


class Subsession(BaseSubsession):

    def creating_session(self):

        if self.round_number == 1:

            #define payment round
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round



            # regroup players: those (a half) who enter first are 1st players(S), others -- 2nd(R)
            matrix_to_get = self.get_group_matrix()
            matrix_to_set = []
            senders_list = []
            receivers_list = []

            if len(matrix_to_get) % 2 == 0:
                for i in range(int(len(matrix_to_get) / 2)):
                    for p in range(2):
                        senders_list.append(matrix_to_get[i][p])
                for i in range(int(len(matrix_to_get) / 2), len(matrix_to_get)):
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

    S_prediction_1 = models.IntegerField(min=0)
    S_prediction_2 = models.IntegerField(min=0)
    S_prediction_3 = models.IntegerField(min=0)
    S_prediction_4 = models.IntegerField(min=0)
    S_prediction_5 = models.IntegerField(min=0)
    S_prediction_6 = models.IntegerField(min=0)
    S_prediction_7 = models.IntegerField(min=0)
    S_prediction_8 = models.IntegerField(min=0)
    S_prediction_9 = models.IntegerField(min=0)
    S_prediction_10 = models.IntegerField(min=0)

    # R answers
    R_prediction = models.IntegerField(min=0)

    R_transfer = models.IntegerField(min=0)


    # set S transfer * factor (note the rounding rules!!)

    mult_transfer = models.IntegerField()

    def gen_mult_transfer(self):
        self.mult_transfer = math.ceil(self.S_transfer * Constants.factors_list[self.round_number - 1])


    # set current payoffs (players don't observe these)

    S_payoff = models.IntegerField()
    R_payoff = models.IntegerField()

    def set_payoffs(self):
        self.S_payoff = Constants.endowments_list[self.round_number - 1] - self.S_transfer + self.R_transfer
        self.R_payoff = self.mult_transfer - self.R_transfer

    S_prediction = models.FloatField()
    S_prediction_payoff = models.FloatField()
    R_prediction_payoff = models.FloatField()

    def prediction_payoffs(self):



        upper_mult_transfer = 0
        self.S_prediction = 0

        list_with_S_predictions = [self.S_prediction_1, self.S_prediction_2, self.S_prediction_3, self.S_prediction_4,
                                   self.S_prediction_5, self.S_prediction_6, self.S_prediction_7, self.S_prediction_8,
                                   self.S_prediction_9, self.S_prediction_10]

        if self.round_number == 1:

            if self.S_transfer <= Constants.predictions_offer_r1[0]:
                upper_mult_transfer = Constants.predictions_return_r1[0]
                self.S_prediction = list_with_S_predictions[0]

            else:
                for i in range(9):
                    if self.S_transfer > Constants.predictions_offer_r1[i] and self.S_transfer <= Constants.predictions_offer_r1[i+1]:
                        upper_mult_transfer = Constants.predictions_return_r1[i+1]
                        self.S_prediction = list_with_S_predictions[i+1]



        if self.round_number == 2:

            if self.S_transfer <= Constants.predictions_offer_r2[0]:
                upper_mult_transfer = Constants.predictions_return_r2[0]
                self.S_prediction = list_with_S_predictions[0]

            else:
                for i in range(9):
                    if self.S_transfer > Constants.predictions_offer_r2[i] and self.S_transfer <= Constants.predictions_offer_r2[i + 1]:
                        upper_mult_transfer = Constants.predictions_return_r2[i + 1]
                        self.S_prediction = list_with_S_predictions[i+1]


        if self.round_number == 3:

            if self.S_transfer <= Constants.predictions_offer_r3[0]:
                upper_mult_transfer = Constants.predictions_return_r3[0]
                self.S_prediction = list_with_S_predictions[0]

            else:
                for i in range(9):
                    if self.S_transfer > Constants.predictions_offer_r3[i] and self.S_transfer <= Constants.predictions_offer_r3[i + 1]:
                        upper_mult_transfer = Constants.predictions_return_r3[i + 1]
                        self.S_prediction = list_with_S_predictions[i+1]




        self.S_prediction_payoff = round((upper_mult_transfer/2) * (1 - abs((self.S_prediction - self.R_transfer)/upper_mult_transfer)), 2)

        # closeness for R predictions about how much S will transfer
        self.R_prediction_payoff = round((Constants.endowments_list[self.round_number - 1]/2) * (1 - abs((self.R_prediction - self.S_transfer)/Constants.endowments_list[self.round_number - 1])), 2)



    # set paying round attributes

    paying_round_num = models.IntegerField()
    pie_size_final = models.IntegerField()
    factor_final = models.FloatField()

    mult_transfer_final = models.FloatField()
    S_prediction_final = models.IntegerField()
    R_transfer_final = models.IntegerField()
    R_prediction_final = models.IntegerField()
    S_transfer_final = models.IntegerField()


    def set_paying_round_attributes(self):

        self.paying_round_num = self.session.vars['paying_round']

        self.pie_size_final = Constants.endowments_list[self.paying_round_num - 1]
        self.factor_final = round(Constants.factors_list[self.paying_round_num - 1],1)

        if self.round_number < self.paying_round_num:
            self.mult_transfer_final = 0
            self.S_prediction_final = 0
            self.R_transfer_final = 0
            self.R_prediction_final = 0
            self.S_transfer_final = 0
        elif self.round_number >= self.paying_round_num:
            self.mult_transfer_final = self.in_round(self.paying_round_num).mult_transfer
            self.S_prediction_final = self.in_round(self.paying_round_num).S_prediction
            self.R_transfer_final = self.in_round(self.paying_round_num).R_transfer
            self.R_prediction_final = self.in_round(self.paying_round_num).R_prediction
            self.S_transfer_final = self.in_round(self.paying_round_num).S_transfer



    # set final payoffs

    S_final_payoff = models.IntegerField()
    R_final_payoff = models.IntegerField()
    S_final_prediction_payoff = models.FloatField()
    R_final_prediction_payoff = models.FloatField()

    S_final_total_payoff = models.FloatField()
    R_final_total_payoff = models.FloatField()

    def set_final_payoffs(self):
        if self.round_number < self.paying_round_num:
            self.S_final_payoff = 0
            self.R_final_payoff = 0
            self.S_final_prediction_payoff = 0
            self.R_final_prediction_payoff = 0
            self.S_final_total_payoff = 0
            self.R_final_total_payoff = 0

        else:
            self.S_final_payoff = self.in_round(self.paying_round_num).S_payoff
            self.R_final_payoff = self.in_round(self.paying_round_num).R_payoff
            self.S_final_prediction_payoff = self.in_round(self.paying_round_num).S_prediction_payoff
            self.R_final_prediction_payoff = self.in_round(self.paying_round_num).R_prediction_payoff
            self.S_final_total_payoff = self.in_round(self.paying_round_num).S_payoff + self.in_round(self.paying_round_num).S_prediction_payoff
            self.R_final_total_payoff = self.in_round(self.paying_round_num).R_payoff + self.in_round(self.paying_round_num).R_prediction_payoff


    # set final payoffs in rub

    def set_payoffs_in_rub(self):
        if self.round_number < self.paying_round_num:
            for p in self.get_players():
                p.payoff = c(0)

        if self.round_number >= self.paying_round_num:
            p1, p2 = self.get_players()[0], self.get_players()[1]
            p1.payoff = c((self.S_final_total_payoff) * Constants.ecu_to_rur) + Constants.participation_payoff
            p2.payoff = c((self.R_final_total_payoff) * Constants.ecu_to_rur) + Constants.participation_payoff



class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1:
            return 'Sender'
        else:
            return 'Receiver'
