from django.db import models
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
class Dht11(models.Model) :
    temp=models.FloatField(null=True)
    hum=models.FloatField(null=True)
    dt=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.temp)

    def save(self, *args, **kwargs):
        if self.temp > 40:
            from DHT.views import sendtele
            sendtele()
            send_mail(
                'température dépasse la normale !!!!' ,
                'anomalie dans la machine la temperature depasse ' + str(self.temp),
                settings.EMAIL_HOST_USER,
                ['atoinifatimaezzahra@gmail.com'],
                fail_silently=False,
            )

        return super().save(*args, **kwargs)

