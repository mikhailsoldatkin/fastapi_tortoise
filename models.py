from tortoise import fields
from tortoise.models import Model


class TariffModel(Model):
    """ Модель Тариф """

    effective_date = fields.DateField(description="Дата вступления в силу")
    cargo_type = fields.CharField(max_length=255, description="Тип груза")
    rate = fields.DecimalField(max_digits=8, decimal_places=3, description="Ставка")

    class Meta:
        table = "tariffs"
        unique_together = (("effective_date", "cargo_type"),)

    def __str__(self):
        return f'Тариф для "{self.cargo_type}" на {self.effective_date}'
