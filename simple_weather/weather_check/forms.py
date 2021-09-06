from django import forms


class ChooseCity(forms.Form):
    cities = [
        ("New York", "New York"),
        ("Paris", "Paris"),
        ("Tokyo", "Tokyo"),
        ("Amsterdam", "Amsterdam"),
        ("Minsk", "Minsk"),
        ("Saint Petersburg", "Saint Petersburg"),
        ("Moscow", "Moscow"),
        ("Rostov-on-don", "Rostov-on-don"),
        ("Yekaterinburg", "Yekaterinburg"),
        ("Kazan", "Kazan"),
        ("Simferopol", "Simferopol"),
        ("Ufa", "Ufa"),
        ("Omsk", "Omsk"),
        ("Krasnodar", "Krasnodar"),
        ("Krasnoyarsk", "Krasnoyarsk"),
        ]

    choosen_city = forms.ChoiceField(
            choices=cities,
            initial='0',
            widget=forms.Select(),
            required=True,
            label='Choose city',
        )


class ChooseStartDate(forms.Form):
    choosen_startdate = forms.DateField(
        required=True,
        help_text="required format: YYYY-MM-DD",
        label="Choose start date"
        )


class ChooseEndDate(forms.Form):
    choosen_enddate = forms.DateField(
        required=True,
        help_text="required format: YYYY-MM-DD",
        label="Choose end date"
        )
