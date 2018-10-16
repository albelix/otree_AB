from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants

class Welcome(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction(Page):
    pass


class NormWaitPage(WaitPage):
    pass



class S_quiz(Page):

    form_model = 'group'
    form_fields = ['S_quiz_1', 'S_quiz_2', 'S_quiz_3', 'S_quiz_4', 'S_quiz_5', 'S_quiz_6', 'S_quiz_7', 'S_quiz_8', ]

    def error_message(self, values):

        if (values["S_quiz_1"] != 75 or values["S_quiz_2"] != 90 or
            values["S_quiz_3"] != 100 or values["S_quiz_4"] != 50 or
            values["S_quiz_5"] != 90 or values["S_quiz_6"] != 45 or
            values["S_quiz_7"] != 65 or values["S_quiz_8"] != 20)  :
            return 'К сожалению, Вы дали неверный ответ. Пожалуйста, прочитайте инструкции еще раз.'

    def is_displayed(self):
        return (self.player.id_in_group == 1 and self.round_number == 1)



class R_quiz(Page):

    form_model = 'group'
    form_fields = ['R_quiz_1', 'R_quiz_2', 'R_quiz_3', 'R_quiz_4', 'R_quiz_5', 'R_quiz_6', 'R_quiz_7', 'R_quiz_8', ]

    def error_message(self, values):

        if (values["R_quiz_1"] != 75 or values["R_quiz_2"] != 90 or
            values["R_quiz_3"] != 100 or values["R_quiz_4"] != 50 or
            values["R_quiz_5"] != 90 or values["R_quiz_6"] != 45 or
            values["R_quiz_7"] != 65 or values["R_quiz_8"] != 20)  :
            return 'К сожалению, Вы дали неверный ответ. Пожалуйста, прочитайте инструкции еще раз.'

    def is_displayed(self):
        return (self.player.id_in_group == 2 and self.round_number == 1)






class S_offer(Page):

    form_model = 'group'
    form_fields = ['S_transfer']

    endowments_list_views = [100, 50, 100]

    def S_transfer_max(self):
        return self.endowments_list_views[self.subsession.round_number - 1]

    def vars_for_template(self):
        dict_with_endowments = {}
        for i in range(3):

            key = 'endowment_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.endowments_list[i]
            key = 'factor_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.factors_list[i]

        return dict_with_endowments

    def is_displayed(self):
        return self.player.id_in_group == 1



class S_prediction(Page):

    form_model = 'group'
    form_fields = ['S_prediction_1', 'S_prediction_2', 'S_prediction_3', 'S_prediction_4', 'S_prediction_5',
                   'S_prediction_6', 'S_prediction_7', 'S_prediction_8', 'S_prediction_9', 'S_prediction_10']

    endowments_list_views = [100, 50, 100]
    predictions_1_list_views = [30, 15, 15]
    predictions_2_list_views = [60, 30, 30]
    predictions_3_list_views = [90, 45, 45]
    predictions_4_list_views = [120, 60, 60]
    predictions_5_list_views = [150, 75, 75]
    predictions_6_list_views = [180, 90, 90]
    predictions_7_list_views = [210, 105, 105]
    predictions_8_list_views = [240, 120, 120]
    predictions_9_list_views = [270, 135, 135]
    predictions_10_list_views = [300, 150, 150]

    def S_prediction_1_max(self):
        return self.predictions_1_list_views[self.subsession.round_number - 1]
    def S_prediction_2_max(self):
        return self.predictions_2_list_views[self.subsession.round_number - 1]
    def S_prediction_3_max(self):
        return self.predictions_3_list_views[self.subsession.round_number - 1]
    def S_prediction_4_max(self):
        return self.predictions_4_list_views[self.subsession.round_number - 1]
    def S_prediction_5_max(self):
        return self.predictions_5_list_views[self.subsession.round_number - 1]
    def S_prediction_6_max(self):
        return self.predictions_6_list_views[self.subsession.round_number - 1]
    def S_prediction_7_max(self):
        return self.predictions_7_list_views[self.subsession.round_number - 1]
    def S_prediction_8_max(self):
        return self.predictions_8_list_views[self.subsession.round_number - 1]
    def S_prediction_9_max(self):
        return self.predictions_9_list_views[self.subsession.round_number - 1]
    def S_prediction_10_max(self):
        return self.predictions_10_list_views[self.subsession.round_number - 1]


    def vars_for_template(self):
        dict_with_endowments = {}
        for i in range(3):

            key = 'endowment_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.endowments_list[i]
            key = 'factor_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.factors_list[i]

        return dict_with_endowments

    def is_displayed(self):
        return self.player.id_in_group == 1






class R_prediction(Page):

    form_model = 'group'
    form_fields = ['R_prediction']

    endowments_list_views = [100, 50, 100]

    def R_prediction_max(self):
        return self.endowments_list_views[self.subsession.round_number - 1]

    def vars_for_template(self):
        dict_with_endowments = {}
        for i in range(3):
            key = 'endowment_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.endowments_list[i]
            key = 'factor_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.factors_list[i]

        return dict_with_endowments

    def is_displayed(self):
        return self.player.id_in_group == 2



class ResultsWaitPage1(WaitPage):

    def after_all_players_arrive(self):
        self.group.gen_mult_transfer()

class R_offer(Page):

    form_model = 'group'
    form_fields = ['R_transfer']

    def R_transfer_max(self):
        return self.group.mult_transfer

    def vars_for_template(self):
        dict_with_endowments = {}
        for i in range(3):
            key = 'endowment_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.endowments_list[i]
            key = 'factor_iter_' + str(i + 1)
            dict_with_endowments[key] = models.Constants.factors_list[i]

        return dict_with_endowments

    def is_displayed(self):
        return self.player.id_in_group == 2

class ResultsWaitPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.prediction_payoffs()
        self.group.set_paying_round_attributes()
        self.group.set_final_payoffs()
        self.group.set_payoffs_in_rub()


class S_final_results(Page):

    def is_displayed(self):
        return (self.player.id_in_group == 1 and self.round_number == 3)

class R_final_results(Page):

   def is_displayed(self):
        return (self.player.id_in_group == 2 and self.round_number == 3)


page_sequence = [
    Welcome,
    Introduction,
    NormWaitPage,
    S_quiz,
    R_quiz,
    NormWaitPage,
    S_offer,
    S_prediction,
    R_prediction,
    ResultsWaitPage1,
    R_offer,
    ResultsWaitPage2,
    S_final_results,
    R_final_results,
    NormWaitPage
]
