from cron_parser.validators.validator import Validator


class Parser:

    def __init__(self, expression):
        self.reasons = []
        self.expression = expression
        self.validator = Validator(self.expression)
