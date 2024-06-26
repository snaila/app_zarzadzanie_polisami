from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from .forms import CarInsuranceModelForm, HouseInsuranceModelForm
from .logic_temp import PolicyPriceCalculator, HousePolicyPriceCalculator
from .models import CarPolicyType, CarInsurance, HousePolicyType, HouseInsurance, CarPolicyFactors


class IndexView(TemplateView):
    template_name = 'index'


class MainPageView(TemplateView):
    template_name = 'main_page'


class OfferCarView(View):
    def get(self, request, *args, **kwargs):
        car_policies = CarPolicyType.objects.all()
        context = {'car_policies': car_policies}
        return render(request, 'offer_car.html', context)


class OfferHouseView(View):
    def get(self, request, *args, **kwargs):
        house_policies = HousePolicyType.objects.all()
        context = {'house_policies': house_policies}
        return render(request, 'offer_house.html', context)


@login_required
def policy_list(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        car_insurances = CarInsurance.objects.filter(customer=customer)
        house_insurances = HouseInsurance.objects.filter(customer=customer)
        return render(request, 'policy_list.html',
                      {'car_insurances': car_insurances, 'house_insurances': house_insurances})
    else:
        return redirect('login')


@login_required
def policy_car_create(request):
    if request.method == "POST":
        car_policy_form = CarInsuranceModelForm(request.POST)
        if car_policy_form.is_valid():
            request.session['car_policy_data'] = request.POST.dict()
            return redirect("policy_car_confirm")
    else:
        car_policy_form = CarInsuranceModelForm()
    return render(request, "policy_car_create.html", {"car_policy_form": car_policy_form})


@login_required
def policy_car_confirm(request):
    if 'car_policy_data' in request.session:
        car_policy_data = request.session['car_policy_data']
        policy_type = car_policy_data.get("policy_type")
        car_policy_form = CarInsuranceModelForm(car_policy_data)

        if car_policy_form.is_valid():
            # Create an instance of PolicyPriceCalculator with form data
            calculator = PolicyPriceCalculator(
                production_year=car_policy_form.cleaned_data['production_year'],
                fuel_factor=CarPolicyFactors.fuel_dict[car_policy_form.cleaned_data['fuel_type']],
                fuel_type=car_policy_form.cleaned_data['fuel_type'],
                mileage=car_policy_form.cleaned_data['mileage'],
                average_year_mileage=car_policy_form.cleaned_data['average_year_mileage'],
                is_rented=car_policy_form.cleaned_data['is_rented'],
                number_of_owners=car_policy_form.cleaned_data['number_of_owners'],
                policy_type=policy_type,
            )

            calculated_price = calculator.calculate_price()

            if request.method == "POST":
                if car_policy_form.is_valid():
                    car_policy = car_policy_form.save(commit=False)
                    car_policy.customer = request.user.customer
                    car_policy.price = calculated_price
                    car_policy.save()
                    del request.session['car_policy_data']
                    messages.success(request, "Gratulacje! Polisa została zawarta!")
                    return redirect("policy_car_detail", policy_id=car_policy.policy_id)
            policy_type_id = car_policy_data.get("policy_type")
            policy_description = CarPolicyType.objects.get(pk=policy_type_id).policy_description

            return render(request, "policy_car_confirm.html",
                          {"car_policy": car_policy_data, "policy_description": policy_description,
                           "calculated_price": calculated_price, })

        else:
            return redirect("policy_car_create")


def policy_car_detail(request, policy_id):
    try:
        car_policy = CarInsurance.objects.get(policy_id=policy_id)
        if not request.user.is_authenticated:
            return render(request, "404.html")
        elif car_policy.customer != request.user.customer:
            return render(request, "404.html")
        policy_description = car_policy.policy_type.policy_description

    except CarInsurance.DoesNotExist:
        return render(request, "404.html")

    ctx = {
        "car_policy": car_policy,
        "policy_description": policy_description,
    }

    return render(request, "policy_car_detail.html", context=ctx)


@login_required
def policy_house_create(request):
    if request.method == "POST":
        house_policy_form = HouseInsuranceModelForm(request.POST)
        if house_policy_form.is_valid():
            request.session['house_policy_data'] = request.POST.dict()
            return redirect("policy_house_confirm")
    else:
        house_policy_form = HouseInsuranceModelForm()
    return render(request, "policy_house_create.html", {"house_policy_form": house_policy_form})


@login_required
def policy_house_confirm(request):
    if 'house_policy_data' in request.session:
        house_policy_data = request.session['house_policy_data']
        policy_type = house_policy_data.get("policy_type")
        house_policy_form = HouseInsuranceModelForm(house_policy_data)

        if house_policy_form.is_valid():
            house_calculator = HousePolicyPriceCalculator(
                house_type=house_policy_form.cleaned_data['house_type'],
                number_of_owners=house_policy_form.cleaned_data['number_of_owners'],
                house_area=house_policy_form.cleaned_data['house_area'],
                house_value=house_policy_form.cleaned_data['house_value'],
                policy_type=policy_type,
            )

            house_calculated_price = house_calculator.calculate_price()

            if request.method == "POST":
                if house_policy_form.is_valid():
                    house_policy = house_policy_form.save(commit=False)
                    house_policy.customer = request.user.customer
                    house_policy.price = house_calculated_price
                    house_policy.save()
                    del request.session['house_policy_data']
                    messages.success(request, "Gratulacje! Polisa została zawarta!")
                    return redirect("policy_house_detail", policy_id=house_policy.policy_id)
            policy_type_id = house_policy_data.get("policy_type")
            policy_description = HousePolicyType.objects.get(pk=policy_type_id).policy_description

            return render(request, "policy_house_confirm.html",
                          {"house_policy": house_policy_data, "policy_description": policy_description,
                           "house_calculated_price": house_calculated_price, })
        else:
            return redirect("policy_house_create")


def policy_house_detail(request, policy_id):
    try:
        house_policy = HouseInsurance.objects.get(policy_id=policy_id)
        if not request.user.is_authenticated:
            return render(request, "404.html")
        elif house_policy.customer != request.user.customer:
            return render(request, "404.html")
        policy_description = house_policy.policy_type.policy_description

    except CarInsurance.DoesNotExist:
        return render(request, "404.html")

    ctx = {
        "house_policy": house_policy,
        "policy_description": policy_description,
    }

    return render(request, "policy_house_detail.html", context=ctx)
