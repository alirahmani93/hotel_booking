from django.db import models


class IntegerChoicesType(models.IntegerChoices):
    pass


def get_name_from_integer_choices(choices: type(IntegerChoicesType), index: int) -> str:
    return choices.names[index]
