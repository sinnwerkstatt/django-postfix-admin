from django.core.exceptions import ValidationError
from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.CharField(max_length=500, blank=True)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def mailboxes(self):
        return self.mailbox_set.all().count()

    def aliases(self):
        return self.alias_set.all().count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Mailbox(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT)
    password = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)

    quota = models.IntegerField(default=0)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}@{}".format(self.name, self.domain.name)

    class Meta:
        unique_together = ('name', 'domain')
        verbose_name_plural = 'Mailboxes'
        ordering = ['name']

    def show_aliases(self):
        return Alias.objects.filter(targets__icontains=f"{self.name}@{self.domain_id}")

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        qs = Alias.objects.filter(name=self.name, domain=self.domain)
        if qs.exists():
            raise ValidationError(
                message=f"An Alias named {self.name}@{self.domain_id} already exists.",
                code='unique_together'
            )


class Alias(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT)
    targets = models.TextField(help_text='You can specify multiple recipients, one per line.')

    description = models.CharField(max_length=500, blank=True)

    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}@{} → {}".format(self.name, self.domain.name, self.targets)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Alias, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        unique_together = ('name', 'domain')
        verbose_name_plural = 'Aliases'
        ordering = ['name']

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        qs = Mailbox.objects.filter(name=self.name, domain=self.domain)
        if qs.exists():
            raise ValidationError(
                message=f"A Mailbox named {self.name}@{self.domain_id} already exists.",
                code='unique_together'
            )


class TLSPolicy(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    POLICY_CHOICES = (
        ('may', 'may'),
        ('encrypt', 'encrypt'),
        ('dane', 'dane'),
        ('dane-only', 'dane-only'),
        ('fingerprint', 'fingerprint'),
        ('verify', 'verify'),
        ('secure', 'secure')
    )
    policy = models.CharField(max_length=20, blank=True, choices=POLICY_CHOICES)
    params = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{}: {} with '{}'".format(self.domain, self.policy, self.params)

    class Meta:
        verbose_name = 'TLS Policy'
        verbose_name_plural = 'TLS Policies'
        ordering = ['domain']
