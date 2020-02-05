from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import re


class GroupingPage(WaitPage):
    group_by_arrival_time = True


class Introduction(Page):
    pass


class RealEffort(Page):
    pass


class Tetris(Page):
    def is_displayed(self):
        if self.session.config['treatment'] == "Tetris":
            return True
        else: 
            return False
    
    form_model = 'player'
    form_fields = ['game_score'] # score currently determined by how many rows are eliminated
    timeout_seconds = 120 #60 # we may want to give players more time 

    def before_next_page(self):
        # for debugging (delete later)
        print(self.player.game_score)
	
class Diamonds(Page):
    def is_displayed(self):
        if self.session.config['treatment'] == "Diamonds":
            return True
        else: 
            return False

    form_model = 'player'
    form_fields = ['diamond_guess', 'diamond_actual']
    timeout_seconds = 60

    def before_next_page(self):
        self.player.game_score = abs(self.player.diamond_guess - self.player.diamond_actual)
        # for debugging (delete later)
        print(self.player.diamond_guess)
        print(self.player.diamond_actual)
        print(self.player.game_score)


class EffortResultsWaitPage(WaitPage):

    # Provisional assignment of scores (This has to be changed to a func that uses the ranking obtained in the real
    # effort game)
    def after_all_players_arrive(self):
        self.group.ranking_income_assignment()
<<<<<<< HEAD
        pass
=======
        self.group.base_income_assignment()
>>>>>>> 7de911a85c4396b075537a278474ab4f908e3e77


class RealEffortResults(Page):

    def vars_for_template(self):
        player = self.player

        effort_or_luck = ""

        if player.shuffled is True:
            effort_or_luck = "Luck"
        elif player.shuffled is False:
            effort_or_luck = "Effort"
        else:
            print("Error: 'player.shuffled' has no value")

        income = player.base_earnings
        ranking = player.ranking

        return {'ranking': ranking, 'income': income, 'effort_or_luck': effort_or_luck}


class PreparingMessage(Page):
    form_model = 'player'
    form_fields = ['message', 'message_receivers']
    # TODO: Exclude our own income from the form fields (this should be done on the html temp)

    def vars_for_template(self):
        player = self.player
#        if player.message == '' and player.message_receivers != 0:
#            return "If you don't want to send a message, choose 0 as the amount of message receivers"
#        
#    def vars_for_template(self):
#        return { 'income_choices': Constants.task_endowments}
        if player.base_earnings < 10:
            string_income = str(player.base_earnings)[:1]
        elif player.base_earnings >= 10:
            string_income = str(player.base_earnings)[:2]

        # ID in group of players with an income of 15
        players15 = []
        # ID in group of players with an income of 25
        players25 = []
        for p in self.group.get_players():
            if p.base_earnings == 15:
                players15.append(p.id_in_group)
            elif p.base_earnings == 25:
                players25.append(p.id_in_group)
            else:
                print("Player of income "+str(p.base_earnings)+" doesn't have 15 or 25 as income")

        if player.id_in_group in players15:
            string_income = string_income + str(players15.index(player.id_in_group))
        elif player.id_in_group in players25:
            string_income = string_income + str(players25.index(player.id_in_group))

        return {'string_income': string_income}


class ProcessingMessage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.base_earnings


class ReceivingMessage(Page):

    def vars_for_template(self):
        player = self.player

        # Obtaining the received messages
        raw_messages = player.messages_received.split(";")
        clean_messages = []

        for item in raw_messages:
            clean_messages.append(item.split(",", 1)[0]) # index out of range error: changed from 1 to 0

        # Loop across received messages in the html in order to show them distinctly (with another color, size, etc)
        return {"received_messages": clean_messages}


class TaxSystem(Page):
    form_model = 'player'
    form_fields = ['preferred_tax_system']

    def before_next_page(self):
        player = self.player
        group = self.group

        if player.preffered_tax_system == 0:
            group.progressivity_votes += 1
        elif player.preffered_tax_system == 1:
            group.tax_rate_votes += 1
        else:
            print("Error: No value for tax_rate_votes")


class TaxDecisionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # Count the number of 0s and 1s. According to that, decide which system is going to be implemented

        group = self.group
        if group.progressivity_votes >= group.tax_rate_votes:
            # System Chosen: Progressivity Sys
            group.tax_policy_system = 0
        elif group.progressivity_votes < group.tax_rate_votes:
            # System Chosen: Tax Rate Sys
            group.tax_policy_system = 1
        else:
            print("Error: No value for Tax Policy System")


class ProgressivityParameter(Page):
    # Displayed only if tax rate sys loses

    form_model = 'player'
    form_fields = ['progressivity']

    def is_displayed(self):
        return self.group.tax_policy_system == 0


class TaxRateParameter(Page):
    # Displayed only if tax rate sys wins

    form_model = 'player'
    form_fields = ['tax_rate']

    def is_displayed(self):
        return self.group.tax_policy_system == 1


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


# There should be a waiting page after preparing the message and before receiving one
page_sequence = [
    GroupingPage,
    Introduction,
    RealEffort,
    Tetris,
	Diamonds, 
    EffortResultsWaitPage,
    RealEffortResults,
    PreparingMessage,
    ProcessingMessage,
    ReceivingMessage,
    TaxSystem,
    TaxDecisionWaitPage,
    ProgressivityParameter,
    TaxRateParameter,
    ResultsWaitPage,
    Results
]
