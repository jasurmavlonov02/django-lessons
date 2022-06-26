from django.shortcuts import render, redirect

from app.forms import CustomerModelForm
from app.models import Customer,Category


# Product list


# customers
def customers(request):
    customer = Customer.objects.all()

    context = {
        'customers': customer
    }

    return render(request, 'app/customers.html', context)


def customer_add(request):
    form = CustomerModelForm()

    if request.method == 'POST':
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('customers')

    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'app/customer-add.html', context)


def customer_details(request, customer_id):
    customer = Customer.objects.filter(id=customer_id).first()
    print(customer)
    context = {
        'customer': customer
    }
    return render(request, 'app/customer-details.html', context)


def customer_delete(request, customer_id):
    customer = Customer.objects.filter(id=customer_id).first()
    if customer:
        customer.delete()
    return redirect('customers')


def customer_update(request, customer_id):
    customer = Customer.objects.filter(id=customer_id).first()
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('customers')

    context = {
        'form': form,
        'action': 'Update'
    }
    return render(request, 'app/customer-update.html', context)
