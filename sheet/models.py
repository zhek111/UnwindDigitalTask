from django.db import models


class Order(models.Model):
    order_number = models.IntegerField(verbose_name="Номер заказа")
    cost = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               verbose_name="Стоимость, $")

    delivery_date = models.DateField(verbose_name="Срок поставки")
    cost_rub = models.DecimalField(max_digits=10,
                                   decimal_places=2,
                                   verbose_name='Стоимость в руб.',
                                   blank=True,
                                   null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.order_number}"
