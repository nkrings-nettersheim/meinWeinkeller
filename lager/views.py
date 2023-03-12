import logging
from django.shortcuts import render
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def index(request):
    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf index.html")
    return render(request, 'lager/index.html', )

def impressum(request):
    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf impressum.html")
    return render(request, 'order/impressum.html')


def datenschutz(request):
    logger.info(f"{request.META.get('HTTP_X_REAL_IP')}; {request.session.session_key}; Aufruf datenschutz.html")
    return render(request, 'order/datenschutz.html')