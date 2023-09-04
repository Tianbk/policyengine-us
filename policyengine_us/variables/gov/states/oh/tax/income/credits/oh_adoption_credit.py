from policyengine_us.model_api import *


class oh_adoption_credit(Variable):
    value_type = float
    entity = Person
    label = "Ohio adoption credit"
    unit = USD
    definition_period = YEAR
    reference = (
        # Ohio 2022 Instructions for Filing Original and Amended - Line 18 – Ohio Adoption Credit
        "https://tax.ohio.gov/static/forms/ohio_individual/individual/2022/it1040-sd100-instruction-booklet.pdf#page=21",
        # Ohio Income - Individual Credits (Education, Displaced Workers & Adoption) 15. - 20.
        "https://tax.ohio.gov/wps/portal/gov/tax/help-center/faqs/income+-+individual+credits/income-individual-credits",
        # The ohio adoption credit has been repealed in the newest revised code, but can still be found in the previous legal code and 2022 tax form
        # 2022 Ohio Revised Code Title 57 | Taxation Chapter 5747 | Income Tax Section 5747.37 | Credit for Legally Adopted Minor Child.
        "https://law.justia.com/codes/ohio/2022/title-57/chapter-5747/section-5747-37/",
    )
    defined_for = StateCode.OH

    def formula(person, period, parameters):
        eligible_adoption_related_expenses = person(
            "qualified_adoption_assistance_expense", period
        )

        p = parameters(period).gov.states.oh.tax.income.credits.adoption
        child_age_eligible = person("age", period) < p.age_threshold
        return min_(
            max_(eligible_adoption_related_expenses, p.minimum_amount),
            p.maximum_amount,
        ) * child_age_eligible
