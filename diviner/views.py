from django.shortcuts import render
from .forms import InvestForm, RetireForm, CommitForm
import math
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'diviner/home.html')


def invest_home(request):
    form = InvestForm()
    return render(request, 'diviner/invest.html', {'form': form})


def format_invest_result(gain):

    gain_formatted = dict()

    gain_formatted['invested_capital'] = "{:,}".format(gain['invested_capital'])
    gain_formatted['future_capital'] = "{:,}".format(gain['future_capital'])
    gain_formatted['capital_gain'] = "{:,}".format(gain['capital_gain'])
    gain_formatted['income_for_life'] = "{:,}".format(gain['income_for_life'])
    gain_formatted['total_return'] = "{0:.2%}".format(gain['total_return'])

    return gain_formatted


def invest_request(request): 
    initial_investment = float(request.GET.get('initial_investment'))
    annual_investment = float(request.GET.get('annual_investment'))
    years = float(request.GET.get('years'))
    annual_interest_rate = float(request.GET.get('annual_interest_rate'))
    invest_result = format_invest_result(invest(initial_investment, annual_investment, years, annual_interest_rate))
    invest_input = dict()
    invest_input['initial_investment'] = "{:,}".format(int(initial_investment))
    invest_input['annual_investment'] = "{:,}".format(int(annual_investment))
    invest_input['years'] = int(years)
    invest_input['annual_interest_rate'] = "{0:.2%}".format(annual_interest_rate)
    return render(request, 'diviner/invest_result.html', {'invest_result': invest_result, 'invest_input': invest_input})


def retire_home(request):
    form = RetireForm()
    return render(request, 'diviner/retire.html', {'form': form})


def format_retire_result(age):

    age_formatted = dict()

    age_formatted['years'] = age['years']
    age_formatted['months'] = age['months']
    age_formatted['days'] = age['days']
    age_formatted['exact_date'] = age['exact_date'].strftime('%A %d %B %Y')

    return age_formatted


def retire_request(request): 
    initial_investment  = float(request.GET.get('initial_investment'))
    annual_investment = float(request.GET.get('annual_investment'))
    income_for_life = float(request.GET.get('income_for_life'))
    annual_interest_rate = float(request.GET.get('annual_interest_rate'))
    retire_result = format_retire_result(retire(initial_investment, annual_investment, income_for_life, annual_interest_rate))
    retire_input = dict()
    retire_input['initial_investment'] = "{:,}".format(int(initial_investment))
    retire_input['annual_investment'] = "{:,}".format(int(annual_investment))
    retire_input['income_for_life'] = "{:,}".format(int(income_for_life))
    retire_input['annual_interest_rate'] = "{0:.2%}".format(annual_interest_rate)
    return render(request, 'diviner/retire_result.html', {'retire_result': retire_result, 'retire_input': retire_input})


def commit_home(request):
    form = CommitForm()
    return render(request, 'diviner/commit.html', {'form': form})


def format_commit_result(commitment):

    commitment_formatted = dict()

    commitment_formatted['total_invested_capital'] = "{:,}".format(commitment['total_invested_capital'])
    commitment_formatted['annual_invested_capital'] = "{:,}".format(commitment['annual_invested_capital'])
    commitment_formatted['monthly_invested_capital'] = "{:,}".format(commitment['monthly_invested_capital'])

    print (commitment_formatted)

    return commitment_formatted


def commit_request(request): 

    initial_investment  = float(request.GET.get('initial_investment'))
    income_for_life = float(request.GET.get('income_for_life'))
    years = float(request.GET.get('years'))
    annual_interest_rate = float(request.GET.get('annual_interest_rate'))
    commit_result = format_commit_result(commit(initial_investment, income_for_life, years, annual_interest_rate))
    commit_input = dict()
    commit_input['initial_investment'] = "{:,}".format(int(initial_investment))
    commit_input['income_for_life'] = "{:,}".format(int(income_for_life))
    commit_input['years'] = int(years)
    commit_input['annual_interest_rate'] = "{0:.2%}".format(annual_interest_rate)
    return render(request, 'diviner/commit_result.html', {'commit_result': commit_result, 'commit_input': commit_input})


def invest(initial_investment, annual_investment, years, annual_interest_rate):
    # invest function returns your financial return given:
    # initial_investment, it's the first dropdown you make at t0
    # annual_investment, it's the amount you commit to inject every year
    # years, your desired investment years
    # annual_interest_rate, it's the annual interest rate you expect to receive from the investment
    periods_per_year = 12
    investment_periods = years * periods_per_year
    periodic_rate = annual_interest_rate / periods_per_year
    periodic_investment = annual_investment / periods_per_year
    
    invested_capital = initial_investment + periodic_investment * investment_periods
    future_capital = initial_investment * (1 + periodic_rate) ** investment_periods + \
                   periodic_investment * (1 + periodic_rate) * \
                   ((1+periodic_rate) ** investment_periods - 1) / \
                   (periodic_rate)
    capital_gain = future_capital - invested_capital 
    total_return = capital_gain / invested_capital
    income_for_life = future_capital * annual_interest_rate
    
    gain = dict()
    
    gain['invested_capital'] = round(int(invested_capital),0)
    gain['future_capital'] = round(int(future_capital),0)
    gain['capital_gain'] = round(int(capital_gain),0)
    gain['income_for_life'] = round(int(income_for_life),0)
    gain['total_return'] = round(total_return,4)
    
    return gain


def retire(initial_investment, annual_investment, income_for_life, annual_interest_rate):
    # retire function returns your retirement date given:
    # initial_investment, it's the first dropdown you make at t0
    # annual_investment, it's the amount you commit to inject every year
    # income_for_life, your desired income for life
    # annual_interest_rate, it's the annual interest rate you expect to receive from the investment
    periods_per_year = 12
    periodic_rate = annual_interest_rate / periods_per_year
    periodic_investment = annual_investment / periods_per_year
    
    log_argument = (periodic_rate * income_for_life + periodic_investment * (1 + periodic_rate) * 
                    annual_interest_rate) / (annual_interest_rate * (periodic_rate * 
                    initial_investment + periodic_investment * (1 + periodic_rate)))
    base = 1 + periodic_rate
    
    investment_years = 1 / periods_per_year * math.log(log_argument, base)
    
    years = int(investment_years)
    months = int((investment_years - years) * 12)
    days = int((investment_years - years - months / 12) * 365.25)
    exact_date = datetime.now().date() + relativedelta(years=years, months=months, days=days)
    
    age = dict()
    
    age['years'] = years
    age['months'] = months
    age['days'] = days
    age['exact_date'] = exact_date
    
    return age


def commit(initial_investment, income_for_life, years, annual_interest_rate):
    # commit function returns your financial commitment given your:
    # initial_investment, it's the first dropdown you make at t0
    # income_for_life, your desired income for life
    # years, your desired investment years
    # annual_interest_rate, it's the annual interest rate you expect to receive from the investment
    periods_per_year = 12
    investment_periods = years * periods_per_year
    periodic_rate = annual_interest_rate / periods_per_year
    
    periodic_investment = (income_for_life / annual_interest_rate - initial_investment * 
                           (1 + periodic_rate) ** investment_periods) * periodic_rate / ((1 + periodic_rate) * 
                           ((1+periodic_rate) ** investment_periods - 1))
    
    annual_invested_capital = periodic_investment * periods_per_year
    monthly_invested_capital = annual_invested_capital / periods_per_year
    total_invested_capital = initial_investment + annual_invested_capital * years
    
    commitment = dict()
    
    commitment['total_invested_capital'] = int(total_invested_capital)
    commitment['annual_invested_capital'] = int(annual_invested_capital)
    commitment['monthly_invested_capital'] = int(monthly_invested_capital)
    
    return commitment