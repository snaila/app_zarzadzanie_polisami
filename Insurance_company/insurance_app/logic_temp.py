from insurance_app.models import current_year, HousePolicyFactors, CarPolicyType, HousePolicyType
from insurance_app.models import CarPolicyFactors


class PolicyPriceCalculator:

    def __init__(self, production_year, fuel_factor, fuel_type, mileage, average_year_mileage, is_rented,
                 number_of_owners, policy_type):
        self.car_policy_factors = CarPolicyFactors.objects.first()
        self.car_policy_type_factors = CarPolicyType.objects.get(policy_type=policy_type)
        self.production_year = production_year
        self.fuel_type = fuel_type
        self.mileage = mileage
        self.average_year_mileage = average_year_mileage
        self.is_rented = is_rented
        self.number_of_owners = number_of_owners
        self.age_factor = (current_year() - production_year) * self.car_policy_factors.age_factor
        self.fuel_factor = self.car_policy_factors.fuel_dict[fuel_type]
        self.policy_type_factor = self.car_policy_type_factors.type_factor

    def mileage_factor_calc(self):
        if self.mileage < 100000:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_1
        elif 100000 < self.mileage < 250000:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_2
        else:
            mileage_factor = (self.mileage // 1000) * self.car_policy_factors.mileage_factor_3
        return mileage_factor

    def avg_mil_factor_calc(self):
        if self.average_year_mileage == 1:
            return self.car_policy_factors.avg_year_mileage_1
        if self.average_year_mileage == 2:
            return self.car_policy_factors.avg_year_mileage_2
        if self.average_year_mileage == 3:
            return self.car_policy_factors.avg_year_mileage_3
        else:
            return self.car_policy_factors.avg_year_mileage_4

    def rented_factor_calc(self):
        if self.is_rented:
            rented_factor = self.car_policy_factors.rented_factor_2
        else:
            rented_factor = self.car_policy_factors.rented_factor_1
        return rented_factor

    def owners_factor_calc(self):
        if self.number_of_owners == 1:
            owners_factor = self.car_policy_factors.owners_factor_2
        elif 2 < self.number_of_owners <= 3:
            owners_factor = self.car_policy_factors.owners_factor_3
        elif 3 < self.number_of_owners > 5:
            owners_factor = self.car_policy_factors.owners_factor_4
        else:
            owners_factor = self.car_policy_factors.owners_factor_1
        return owners_factor

    def calculate_price(self):
        return round(((
                              self.car_policy_factors.base +
                              (self.fuel_factor * self.mileage_factor_calc() +
                               self.avg_mil_factor_calc() * self.rented_factor_calc() * self.owners_factor_calc()) * self.policy_type_factor
                              - self.age_factor) * 2),
                     2)


class HousePolicyPriceCalculator:

    def __init__(self, house_type, number_of_owners, house_area, house_value, policy_type):
        self.house_policy_factors = HousePolicyFactors.objects.first()
        self.house_policy_type_factors = HousePolicyType.objects.get(policy_type=policy_type)
        self.number_of_owners = number_of_owners
        self.house_area = house_area
        self.house_value = house_value
        self.house_type = house_type
        self.house_type_factors = self.house_policy_factors.house_dict[house_type]
        self.policy_house_type_factor = self.house_policy_type_factors.type_factor

    def house_area_calc(self):
        if self.house_area <= 30:
            house_area_factor = self.house_area * self.house_policy_factors.house_area_factor_1
        elif 30 < self.house_area < 50:
            house_area_factor = self.house_area * self.house_policy_factors.house_area_factor_2
        else:
            house_area_factor = self.house_area * self.house_policy_factors.house_area_factor_3
        return house_area_factor

    def house_value_calc(self):
        if self.house_value <= 600000:
            house_value_factor = (self.house_value / 1000) * self.house_policy_factors.house_value_factor_1
        elif 600000 < self.house_value < 1200000:
            house_value_factor = (self.house_value / 1000) * self.house_policy_factors.house_value_factor_2
        else:
            house_value_factor = (self.house_value / 1000) * self.house_policy_factors.house_value_factor_3
        return house_value_factor

    def house_owners_factor_calc(self):
        if self.number_of_owners > 1:
            house_owners_factor = self.house_policy_factors.house_owners_factor_2
        elif 1 < self.number_of_owners <= 3:
            house_owners_factor = self.house_policy_factors.house_owners_factor_3
        elif self.number_of_owners > 3:
            house_owners_factor = self.house_policy_factors.house_owners_factor_4
        else:
            house_owners_factor = self.house_policy_factors.house_owners_factor_1
        return house_owners_factor

    def calculate_price(self):
        return round(((
                              self.house_policy_factors.base + self.house_area_calc() + self.house_value_calc() +
                              self.house_owners_factor_calc() * 10 * self.policy_house_type_factor) / 10 * 2),
                     3)
