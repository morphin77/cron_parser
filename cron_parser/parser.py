from cron_parser.validators.validator import Validator


class Parser:
    def __init__(self, expression):
        self.expression = expression
        self.validator: Validator = Validator(self.expression)
