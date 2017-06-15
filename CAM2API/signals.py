from django.dispatch import Signal

#define a customized signal
account_created = Signal(providing_args=['username'])