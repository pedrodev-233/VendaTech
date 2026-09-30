from django.shortcuts import render

# Create your views here.
def index(request):
    print('Servidor iniciado com sucesso!')
    
    return render(request, 'core/index.html')