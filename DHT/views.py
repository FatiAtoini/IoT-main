import csv

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
from django.utils import timezone
import telepot
from DHT.models import Dht11
import urllib3
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating the user
        user = authenticate(request, username=username, password=password)
        # Checking if authentication is successful
        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
def logout_user(request):
    logout(request)
    return redirect('/')


# Create your views here.
@login_required
def table(request):
    #derniere_ligne=Dht11.objects.last()
    #derniere_date = Dht11.objects.last().dt
    #delta_temps=timezone.now() - derniere_date
   # difference_minutes=delta_temps.seconds //60
    #temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    #if difference_minutes > 60:
      #  temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
      # valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp':derniere_ligne.temp, 'hum': derniere_ligne.hum}
       #valeurs=['valeurs', Dht11.objects.all]


        tab = Dht11.objects.all()


        s={'tab':tab}
        #return render(request, 'chart.html', {'valeurs': valeurs})


        return render(request, 'chart.html', s)


#pour afficher navbar de template
@login_required
def index_view(request):
    tab = Dht11.objects.all()

    s = {'tab': tab}
    return render(request, 'index.html',s)
@login_required
def chart_view(request):

    return render(request, 'chart.html')
@login_required
def table_view(request):
    tab = Dht11.objects.all()

    s = {'tab': tab}
    return render(request, 'table.html',s)
@login_required
def base_view(request):
    tab = Dht11.objects.all()
    s = {'tab': tab}
    return render(request, 'base.html', s)



@login_required
def chart_data(request):
    dht = Dht11.objects.all()
    data = {
    'temps': [Dt.dt for Dt in dht],
     'temperature': [Temp.temp for Temp in dht],
     'humidity': [Hum.hum for Hum in dht]
     }
    return JsonResponse(data)



@login_required
def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
@login_required
def chart_data_period(request, period):
    if period == 'jour':
        return chart_data_jour(request)
    elif period == 'semaine':
        return chart_data_semaine(request)
    elif period == 'mois':
        return chart_data_mois(request)
    else:
        # Handle invalid period
        return JsonResponse({'error': 'Invalid period'}, status=400)
@login_required
def chart_data_jour(request):
 dht = Dht11.objects.all()
 now = timezone.now()

# Récupérer l'heure il y a 24 heures
 last_24_hours = now - timezone.timedelta(hours=24)

# Récupérer tous les objets de Module créés au cours des 24 dernières heures
 dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
 data = {
            'temps': [Dt.dt for Dt in dht],
            'temperature': [Temp.temp for Temp in dht],
            'humidity': [Hum.hum for Hum in dht]
    }
 return JsonResponse(data)
@login_required
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#
#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
@login_required
def chart_data_mois(request):
    dht = Dht11.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

def sendtele():

    token = '6964170219:AAEp2jeHvcOh-IiKxdb_mUgpfA84HVdhY2E'
    rece_id = 1445830546
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale !!!')