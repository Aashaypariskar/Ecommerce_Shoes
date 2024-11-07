from django.shortcuts import render,redirect

def index(request):
    return render(request,'core/index.html')

def product(request,id):
    return render(request,'core/product.html', {'id':id})