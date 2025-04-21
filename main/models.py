from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enter(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Enter'
        verbose_name_plural = 'Enters'
        ordering = ['-created_at']

class EnterItem(models.Model):
    enter = models.ForeignKey(Enter, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'EnterItem'
        verbose_name_plural = 'EnterItems'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # old = 0
        # if self.id:
        #     old = type(self).objects.get(id=self.id).quantity

        # self.product.quantity += self.quantity - old
        # self.product.save()

        if self.id:
            self.product.quantity -= EnterItem.objects.get(id=self.id).quantity
        self.product.quantity += self.quantity
        self.product.save()

        super().save(*args, **kwargs)

class Out(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Out'
        verbose_name_plural = 'Outs'
        ordering = ['-created_at']

class OutItem(models.Model):
    out = models.ForeignKey(Out, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'OutItem'
        verbose_name_plural = 'OutItems'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        old = 0
        if self.id:
            old = type(self).objects.get(id=self.id).quantity

        self.product.quantity -= self.quantity - old
        self.product.save()
        super().save(*args, **kwargs)