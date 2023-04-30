from django.db import models

from accounts.models import User
from crypto.models import Crypto


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
