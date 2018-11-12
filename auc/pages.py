from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Role(Page):
    pass


class ResultsWaitPage1(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_valuations()

class Valuation(Page):
    pass

class Subrole(Page):
    form_model = 'player'
    form_fields = ['subrole']


class ResultsWaitPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.valuation_announcement()

class Bids_Sellers(Page):

    def is_displayed(self):
        return (self.player.role() == "Seller" and self.player.subrole == "participant"
                and self.group.bs_auc_ind == 1)

    form_model = 'player'
    form_fields = ['sellerchoice', 'sellerbid']

    def sellerchoice_choices(self):
        bs_auc_id_list = [int(s) for s in self.group.bs_auc_id_str.split()]
        bs_auc_values_list = [float(s) for s in self.group.bs_auc_val_str.split()]
        list_of_choices = []
        for i in range(len(bs_auc_id_list)):
            choice = [bs_auc_id_list[i], bs_auc_values_list[i]]
            list_of_choices.append(choice)
        return list_of_choices

class No_Bids_Sellers(Page):

    def is_displayed(self):
        return (self.player.role() == "Seller" and self.player.subrole == "participant"
                and self.group.bs_auc_ind == 0)

class Bids_Buyers(Page):

    def is_displayed(self):
        return (self.player.role() == "Buyer" and self.player.subrole == "participant"
                and self.group.ss_auc_ind == 1)

    form_model = 'player'
    form_fields = ['buyerchoice', 'buyerbid']

    def buyerchoice_choices(self):
        ss_auc_id_list = [int(s) for s in self.group.ss_auc_id_str.split()]
        ss_auc_values_list = [float(s) for s in self.group.ss_auc_val_str.split()]
        list_of_choices = []
        for i in range(len(ss_auc_id_list)):
            choice = [ss_auc_id_list[i], ss_auc_values_list[i]]
            list_of_choices.append(choice)
        return list_of_choices

class No_Bids_Buyers(Page):
    def is_displayed(self):
        return (self.player.role() == "Buyer" and self.player.subrole == "participant"
                and self.group.ss_auc_ind == 0)


class NormWaitPage(WaitPage):
    pass

class ResultsWaitPage3(WaitPage):
    def after_all_players_arrive(self):
        self.group.SPSB()

class Results(Page): #added, was: pass
    def vars_for_template(self):
        self.player.my_method()
        return {
            'my_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
        }


page_sequence = [
    Role,
    ResultsWaitPage1,
    Valuation,
    Subrole,
    ResultsWaitPage2,
    Bids_Sellers,
    No_Bids_Sellers,
    Bids_Buyers,
    No_Bids_Buyers,
    NormWaitPage,
    ResultsWaitPage3,
    Results
]
