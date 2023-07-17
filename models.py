from tortoise import fields
from tortoise.models import Model


class TariffModel(Model):
    """ Модель Тариф """

    effective_date = fields.DateField()
    cargo_type = fields.CharField(max_length=255)
    rate = fields.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        table = "tariffs"
        unique_together = (("effective_date", "cargo_type"),)
