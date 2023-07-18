from django.shortcuts import render

# Create your views here.
def customer_index(request):
    return render(request,'Customer/CustomerIndex.html',{})
