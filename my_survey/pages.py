from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'field',
                   'height',
                   'city',
                   'yearsinmsc',
                   'expect',
                   'othercit',
                   'riskat',
                   'income',
                   'satis',
                   'trust',
                   'freedom',
                   ]


# class City(Page):
#     form_model = 'player'
#     form_fields = ['city',
#                    'yearsinmsc', 'mscyourcity', 'achieve', 'deput']


# class Yourself(Page):
#     form_model = 'player'
#     form_fields = ['univ',
#                    'study',
#                    'riskat',
#                    'riskHL1',
#                    'riskHL2',
#                    'riskHL3',
#                    'riskHL4',
#                    'riskHL5',
#                    'riskHL6',
#                    'riskHL7',
#                    'riskHL8',
#                    'riskHL9',
#                    'riskHL10',
# #                   'income',
#                    'satis',
#                    'trust',
#                    'freedom']

# class polit(Page):
#     form_model = 'player'
#     form_fields = ['freedom',
#                        'politics',
#                        'leftright',
#                        'owner',
#                        'responsibility',
#                        'democracy',
#                         'democracy_today',
#                         'renovation',
#                         'attitudes']

    def before_next_page(self):
        self.player.set_payoff()


page_sequence = [
    MyPage #, Yourself #, polit, City,
]
