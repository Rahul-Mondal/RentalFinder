from django.db import models

class User(models.Model):

    class Meta:
        verbose_name_plural = "User"
        unique_together = (("email", "user_type"),)

    TYPE = (
        ('O', 'Owner'),
        ('R', 'Renter'),
    )
    name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=1, choices=TYPE)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return '%s' % self.name


class Property(models.Model):

    class Meta:
        verbose_name_plural = "Property"
        unique_together = (("zip", "owner"),("property_name", "owner"),)

    P_TYPE= (
        ('C', 'Condo'),
        ('S', 'Studio'),
    )
    type = models.CharField(max_length=1, choices=P_TYPE)
    property_name = models.CharField(max_length=50)
    street_name = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    state = models.CharField(max_length=2)
    price = models.PositiveIntegerField()
    renter = models.ForeignKey('User', limit_choices_to={'user_type': 'R'},
                               on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='renter_users')
    owner = models.ForeignKey('User', limit_choices_to={'user_type': 'O'},
                              on_delete=models.CASCADE, related_name='owner_users')

    def __str__(self):
        return '%s in %s %s' % (self.property_name, self.state, self.zip)

    def save(self, *args, **kwargs):
        if self.renter:
            if self.renter.email == self.owner.email:
                raise Exception('owner and renter cannot be same for a particular property')
        super(Property, self).save(*args, **kwargs)