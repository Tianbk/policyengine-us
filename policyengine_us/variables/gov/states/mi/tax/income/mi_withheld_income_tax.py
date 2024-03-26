from policyengine_us.model_api import *


class mi_withheld_income_tax(Variable):
    value_type = float
    entity = Person
    label = "Michigan withheld income tax"
    defined_for = StateCode.MI
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        employment_income = person("irs_employment_income", period)
        p = parameters(period).gov.states.mi.tax.income
        # The MI standard deduction only applys for elderly
        # Wo do not apply deductions here
        return p.rate * employment_income
