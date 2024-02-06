import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import plotly.graph_objects as go
import plotly.offline as plotly_offline
from django import forms
from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


def home(request):
    # Your logic to render the home page
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('predict')  # Redirect to the predict page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, "login.html")


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Create a new user with the provided username and password
        user = User.objects.create_user(username=username, password=password)
        if user:
            return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Failed to create a new user.'})
    else:
        return render(request, "signup.html")
@login_required
def predict(request):
    return render(request, "predict.html")


@login_required
def predict(request):
    if request.method == 'POST':
        data = pd.read_csv("C:\\Users\\Mochah Tech\\Desktop\\USA_Housing.csv")
        data = data.drop(['Address'], axis=1)
        X = data.drop('Price', axis=1)
        Y = data['Price']
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.30)
        model = LinearRegression()
        model.fit(X_train, Y_train)

        var1 = float(request.POST.get('n1'))
        var2 = float(request.POST.get('n2'))
        var3 = float(request.POST.get('n3'))
        var4 = float(request.POST.get('n4'))
        var5 = float(request.POST.get('n5'))

        pred = model.predict(np.array([var1, var2, var3, var4, var5]).reshape(1, -1))
        pred = round(pred[0])

        price = "Predicted price is MWK " + str(pred)
        return render(request, "predict.html", {"result2": price})

    return render(request, "predict.html")

@login_required
def result(request):
    data = pd.read_csv("C:\\Users\\Mochah Tech\\Desktop\\USA_Housing.csv")
    data = data.drop(['Address'], axis=1)
    x_columns = ['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 'Avg. Area Number of Bedrooms', 'Area Population']
    y_column = 'Price'

    X = data[x_columns]
    Y = data[y_column]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.30)
    model = LinearRegression()
    model.fit(X_train, Y_train)

    var1 = float(request.GET['n1'])
    var2 = float(request.GET['n2'])
    var3 = float(request.GET['n3'])
    var4 = float(request.GET['n4'])
    var5 = float(request.GET['n5'])

    pred = model.predict([[var1, var2, var3, var4, var5]])
    pred = round(pred[0], 2)

    price = "Predicted price is MWK " + str(pred)

    return render(request, "predict.html", {"result2": price})

def graph_view(request):
    return render(request, 'graph.html')


def user_logout(request):
    logout(request)
    return redirect('login')


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject,
                f'Name: {name}\nEmail: {email}\n\nMessage: {message}',
                email,
                ['kevinbinali6@gmail.com'],  # Replace with your predefined email address
                fail_silently=False
            )
            return render(request, 'feedback/thank_you.html')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})



def about_us(request):
    return render(request, 'about_us.html')