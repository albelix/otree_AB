from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

   def play_round(self):
        contr = random.randint(0, Constants.endowment)
        yield (pages.Contribution, {'contribution': contr})
        yield (pages.Results0)
        yield (pages.Results)
        if self.round_number == Constants.num_rounds:
            yield (pages.ResultsSummary)
