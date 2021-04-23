from django.shortcuts import render


def main(request):
    return render(request, 'store/main.html')