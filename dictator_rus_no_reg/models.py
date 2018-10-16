from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from random import shuffle


doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'D'
    players_per_group = 2
    num_rounds = 6

    instructions_template = 'dictator_rus_no_reg/Instructions.html'

    endowments_list = [60, 60, 60, 100, 100, 100]
    unit_values_for_S_list = [1, 1, 3, 1, 3, 1]
    unit_values_for_R_list = [1, 3, 1, 3, 1, 1]
    ecu_to_rur = 2


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            #define the paying round
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round

            #define the random order of the pie size and ecu rate
            initial_order_list = [0, 1, 2, 3, 4, 5]
            shuffle(initial_order_list)
            random_order_list = initial_order_list
            self.session.vars['treatment_1'] = random_order_list[0]
            self.session.vars['treatment_2'] = random_order_list[1]
            self.session.vars['treatment_3'] = random_order_list[2]
            self.session.vars['treatment_4'] = random_order_list[3]
            self.session.vars['treatment_5'] = random_order_list[4]
            self.session.vars['treatment_6'] = random_order_list[5]



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

    #quiz

    S_quiz_1 = models.IntegerField()
    S_quiz_2 = models.IntegerField()

    R_quiz_1 = models.IntegerField()
    R_quiz_2 = models.IntegerField()
    R_quiz_3 = models.IntegerField()
    R_quiz_4 = models.IntegerField()


    # S answers

    S_transfer = models.IntegerField(min=0)
    S_self_part = models.IntegerField(min=0)

    S_prediction = models.IntegerField(min=0)


    # R answers

    R_prediction = models.IntegerField(min=0)

    R_min_offer = models.IntegerField(min=0)

    # set round attributes (players don't observe these)
    pie_size = models.IntegerField()
    unit_value_for_S = models.IntegerField()
    unit_value_for_R = models.IntegerField()

    def set_round_attributes(self):
        treatment_key = 'treatment_' + str(self.round_number)
        treatment_num = self.session.vars[treatment_key]

        self.pie_size = Constants.endowments_list[treatment_num]
        self.unit_value_for_S = Constants.unit_values_for_S_list[treatment_num]
        self.unit_value_for_R = Constants.unit_values_for_R_list[treatment_num]

    # set S and R current payoffs (players don't observe these)

    S_payoff_tokens = models.IntegerField()
    R_payoff_tokens = models.IntegerField()
    S_payoff_ecu = models.IntegerField()
    R_payoff_ecu = models.IntegerField()

    def set_payoffs(self):

        #define the pie size and ecu rate treatment
        treatment_key = 'treatment_' + str(self.round_number)
        treatment_num = self.session.vars[treatment_key]

        # define the payoffs (tokens)
        self.S_payoff_tokens = Constants.endowments_list[treatment_num] - self.S_transfer
        self.R_payoff_tokens = self.S_transfer

        # define the payoffs (ecu)
        self.S_payoff_ecu = self.S_payoff_tokens * Constants.unit_values_for_S_list[treatment_num]
        self.R_payoff_ecu = self.R_payoff_tokens * Constants.unit_values_for_R_list[treatment_num]


    # set S and R current prediction payoffs (players don't observe these)

    S_prediction_payoff_tokens = models.FloatField()
    R_prediction_payoff_tokens = models.FloatField()
    S_prediction_payoff_ecu = models.FloatField()
    R_prediction_payoff_ecu = models.FloatField()

    def prediction_payoffs(self):

        # define the pie size and ecu rate treatment
        treatment_key = 'treatment_' + str(self.round_number)
        treatment_num = self.session.vars[treatment_key]

        # define the prediction payoffs (tokens)
        self.S_prediction_payoff_tokens = round((Constants.endowments_list[treatment_num]/2)*(1-abs((self.S_prediction - self.R_min_offer)/Constants.endowments_list[treatment_num])), 2)
        self.R_prediction_payoff_tokens = round((Constants.endowments_list[treatment_num]/2)*(1-abs((self.R_prediction - self.S_transfer)/Constants.endowments_list[treatment_num])),2)


        # define the prediction payoffs (ecu)
        self.S_prediction_payoff_ecu = round(self.S_prediction_payoff_tokens * Constants.unit_values_for_S_list[treatment_num],2)
        self.R_prediction_payoff_ecu = round(self.R_prediction_payoff_tokens*Constants.unit_values_for_R_list[treatment_num],2)




    # set paying round attributes

    paying_round_num = models.IntegerField()
    pie_size_final = models.IntegerField()
    unit_value_for_S_final = models.IntegerField()
    unit_value_for_R_final = models.IntegerField()

    S_prediction_final = models.IntegerField()
    R_min_offer_final = models.IntegerField()
    R_prediction_final = models.IntegerField()
    S_transfer_final = models.IntegerField()


    def set_paying_round_attributes(self):

        self.paying_round_num = self.session.vars['paying_round']

        treatment_key = 'treatment_' + str(self.session.vars['paying_round'])
        treatment_num = self.session.vars[treatment_key]

        self.pie_size_final = Constants.endowments_list[treatment_num]
        self.unit_value_for_S_final = Constants.unit_values_for_S_list[treatment_num]
        self.unit_value_for_R_final = Constants.unit_values_for_R_list[treatment_num]

        if self.round_number < self.paying_round_num:
            self.S_prediction_final = 0
            self.R_min_offer_final = 0
            self.R_prediction_final = 0
            self.S_transfer_final = 0
        elif self.round_number >= self.paying_round_num:
            self.S_prediction_final = self.in_round(self.paying_round_num).S_prediction
            self.R_min_offer_final = self.in_round(self.paying_round_num).R_min_offer
            self.R_prediction_final = self.in_round(self.paying_round_num).R_prediction
            self.S_transfer_final = self.in_round(self.paying_round_num).S_transfer

    # set S and R final payoffs and prediction payoffs (players observe these in the end)

    S_final_payoff_tokens = models.IntegerField()
    R_final_payoff_tokens = models.IntegerField()
    S_final_payoff_ecu = models.IntegerField()
    R_final_payoff_ecu = models.IntegerField()

    S_final_prediction_payoff_tokens = models.FloatField()
    R_final_prediction_payoff_tokens = models.FloatField()
    S_final_prediction_payoff_ecu = models.FloatField()
    R_final_prediction_payoff_ecu = models.FloatField()

    def set_final_payoffs(self):

        if self.round_number < self.paying_round_num:
            self.S_final_payoff_tokens = 0
            self.R_final_payoff_tokens = 0
            self.S_final_payoff_ecu = 0
            self.R_final_payoff_ecu = 0

            self.S_final_prediction_payoff_tokens = 0
            self.R_final_prediction_payoff_tokens = 0
            self.S_final_prediction_payoff_ecu = 0
            self.R_final_prediction_payoff_ecu = 0

        elif self.round_number >= self.paying_round_num:

            self.S_final_payoff_tokens = self.in_round(self.paying_round_num).S_payoff_tokens
            self.R_final_payoff_tokens = self.in_round(self.paying_round_num).R_payoff_tokens
            self.S_final_payoff_ecu = self.in_round(self.paying_round_num).S_payoff_ecu
            self.R_final_payoff_ecu = self.in_round(self.paying_round_num).R_payoff_ecu

            self.S_final_prediction_payoff_tokens = self.in_round(self.paying_round_num).S_prediction_payoff_tokens
            self.R_final_prediction_payoff_tokens = self.in_round(self.paying_round_num).R_prediction_payoff_tokens
            self.S_final_prediction_payoff_ecu = self.in_round(self.paying_round_num).S_prediction_payoff_ecu
            self.R_final_prediction_payoff_ecu = self.in_round(self.paying_round_num).R_prediction_payoff_ecu

            self.R_final_payoff = self.R_final_payoff_ecu + self.R_final_prediction_payoff_ecu
            self.S_final_payoff = self.S_final_payoff_ecu + self.S_final_prediction_payoff_ecu

    # set word forms

    S_payoff_form = models.StringField()
    R_payoff_form = models.StringField()
    S_prediction_form = models.StringField()
    R_min_offer_form = models.StringField()
    R_prediction_form = models.StringField()
    S_transfer_form = models.StringField()
    S_final_payoff = models.IntegerField()
    R_final_payoff = models.IntegerField()

    def set_linguistic_forms(self):

        def linguistic(var_to_check):

            form1_list = ['1']
            form2_list = ['2', '3', '4']
            form3_list = ['11', '12', '13', '14']

            word_form = ''

            if len(str(var_to_check)) == 1:
                if str(var_to_check) in form1_list:
                    word_form = 'токен'
                elif str(var_to_check) in form2_list:
                    word_form = 'токена'
                else:
                    word_form = 'токенов'

            elif len(str(var_to_check)) > 1:
                nums_to_check_1 = str(var_to_check)[-1]
                nums_to_check_2 = str(var_to_check)[-2:]
                if nums_to_check_2 in form3_list:
                    word_form = 'токенов'
                else:
                    if nums_to_check_1 in form1_list:
                        word_form = 'токен'
                    elif nums_to_check_1 in form2_list:
                        word_form = 'токена'
                    else:
                        word_form = 'токенов'
            return word_form

        self.S_payoff_form = linguistic(self.S_final_payoff_tokens)
        self.R_payoff_form = linguistic(self.R_final_payoff_tokens)

        self.S_prediction_form = linguistic(self.S_prediction_final)
        self.R_min_offer_form = linguistic(self.R_min_offer_final)
        self.R_prediction_form = linguistic(self.R_prediction_final)
        self.S_transfer_form = linguistic(self.S_transfer_final)


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'Sender'
        else:
            return 'Receiver'


