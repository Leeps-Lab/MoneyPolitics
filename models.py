from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)

import controls as ctrl
import random

author = 'Marco Gutierrez and Skyler Stewart'

doc = """
Money and Politics App
"""


class Constants(BaseConstants):
    name_in_url = 'DecisionStudy'
    players_per_group = 9
    num_rounds = 1

    # There are some parameters that may vary during the development of this app. In order to make this as soft coded as
    # possible, the code should be flexible enough to allow changes in this ones and obtain them from an external
    # .py/txt file (If you find a better way, feel free to update the code with it)
    task_endowments = ctrl.task_endowments
    number_of_messages = ctrl.number_of_messages
    message_cost = ctrl.message_cost
    # Maximum endowment considered for a player to be in "poverty"
    poverty_line = ctrl.poverty_line
    # Possible Tax Systems
    possible_tax_systems = ctrl.possible_tax_systems


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    # Amount of players who will receive a luck based income
    lucky_players = models.IntegerField()

    # Votes for Tax Policy Systems
    progressivity_votes = models.IntegerField()
    tax_rate_votes = models.IntegerField()

    # Chosen Tax Policy System
    tax_policy_system = models.IntegerField(choices=Constants.possible_tax_systems)

    # Amount collected after the tax policy parameter has been decided
    tax_revenue = models.CurrencyField(min=0)

    def choosing_message_receiver(self):
        receivers = []
        for p in self.get_players():
            if p.real_effort_earnings <= Constants.poverty_line:
                receivers.append(p.id_in_group)

        # To select randomly the ones that will receive the messages (Note that with this, ff the first one on the
        # list receives one message, he will receive the other ones too)
        random.SystemRandom().shuffle(receivers)
        return receivers


class Player(BasePlayer):

    # Real Effort Earnings
    real_effort_earnings = models.CurrencyField(min=0)

    # Ranking on real effort task
    ranking = models.IntegerField(min=1, max=9)

    # Shuffled == True if player's income will be shuffled, False if not
    shuffled = models.BooleanField()

    # Earnings after the shuffling
    base_earnings = models.CurrencyField(min=0)

    # Message to be sent (It should only have 500 characters. This has been implemented on PreparingMessage.html)
    message = models.CharField(max_length=500, label='Write the message you want to send (max. 500 characters)')
    # Amount of receivers of player's message (players with 9 or 15)
    amount_message_receivers = models.IntegerField(min=0, max=Constants.players_per_group, label='Write your preferred '
                                                                                                 'number of message '
                                                                                                 'receivers')
    # Id of players who received the message of an specific player
    messages_receivers = models.StringField(initial="")

    messages_received = models.StringField(initial="")
    # Number of messages received
    amount_messages_received = models.IntegerField(min=0)
    # Total cost for sending the messages
    total_messaging_costs = models.CurrencyField()

    preferred_tax_system = models.CharField(choices=Constants.possible_tax_systems)
    # Preferred Tax Policy Parameters
    progressivity = models.FloatField(min=0)
    tax_rate = models.FloatField(min=0)
