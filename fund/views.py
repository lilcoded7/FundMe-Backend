from django.shortcuts import render, get_object_or_404
from fund.models.phila_fund import PhilaFund
from fund.models.category import Category
from fund.models.volunteers import Volunteer

# Create your views here.


def home(request):
    philafund = PhilaFund.objects.all()
    categories = Category.objects.all()
    volunteers = Volunteer.objects.all()

    context = {
        'philafund':philafund,
        'categories':categories,
        'volunteers':volunteers
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')



def causes(request, causes_id):
    category = get_object_or_404(Category, id=causes_id)

    causes = PhilaFund.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'main/causes.html', {'causes':causes, 'category':category, 'categories':categories})


def causes_details(request, causes_id):
    causes = get_object_or_404(PhilaFund, id=causes_id)
    categories = Category.objects.all()

    return render(request, 'main/causes_details.html', {'causes':causes, 'categories':categories})