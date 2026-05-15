from django import forms


class CalcForm(forms.Form):
    num1 = forms.FloatField(label='Перше число')

    sign = forms.ChoiceField(label='Операція', choices=[
        ('+', '+'),
        ('-', '-'),
        ('*', '*'),
        ('/', '/'),
        ('ctg', 'ctg')
    ])

    num2 = forms.FloatField(label='Друге число', required=False)

    precision = forms.IntegerField(label='Точність (знаків)', initial=2, min_value=0)
