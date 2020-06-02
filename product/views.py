from django.shortcuts import render , get_object_or_404
from django.core.paginator import Paginator

# Create your views here.
from .models import Product

def product_list(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 4)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    context = {'product_list' : product_list}
    return render(request , 'Product/product_list.html' , context)

def product_detail(request , slug):
    #product_detail = Product.objects.get(PRDSlug=slug)
    product_detail = get_object_or_404(Product , PRDSlug=slug)
    context = {'product_detail' : product_detail}
    return render(request , 'Product/product_detail.html' , context)
