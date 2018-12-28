from django import forms
from .models import InvestChoice, RetireChoice, CommitChoice

class InvestForm(forms.ModelForm):

    class Meta:
        model = InvestChoice
        fields = ('initial_investment', 'annual_investment', 'years', 'annual_interest_rate',)


class RetireForm(forms.ModelForm):

    class Meta:
        model = RetireChoice
        fields = ('initial_investment', 'annual_investment', 'income_for_life', 'annual_interest_rate',)


class CommitForm(forms.ModelForm):

    class Meta:
        model = CommitChoice
        fields = ('initial_investment', 'income_for_life', 'years', 'annual_interest_rate',)