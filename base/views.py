from django.shortcuts import render, redirect
from django.views import View
from .models import Listing
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import ListingForm, RegisterForm
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.hashers import make_password
from django.urls import reverse


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('search')
        tag = request.GET.get('tag')
        if(q is not None):
            if(q):
                listings = Listing.objects.filter(title__icontains=q)
            else:
                listings = ''
        elif(tag is not None):
            if(tag):
                listings = Listing.objects.filter(tags__name__in=[tag])
            else:
                listings = ''
        else:
            listings = Listing.objects.prefetch_related('tags').all()


        return render(request, self.template_name, {'listings':listings})

    # def post(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {'form': form})


class ListingsView(View):
    template_name = 'listings.html'

    def get(self, request, *args, **kwargs):
        listings = Listing.objects.prefetch_related('tags').all()
        # search = request.GET.get('search')
        return render(request, self.template_name, {'listings': listings})

    # def post(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {'form': form})



class ListingView(View):
    template_name = 'listing.html'

    def get(self, request,pk, *args, **kwargs):
        print(args)
        listing = Listing.objects.get(id=pk)
        tags = listing.tags.names()
        return render(request, self.template_name, {'listing': listing, 'tags': tags})

    # def post(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                User.objects.get(username=username)
            except:
                messages.error(request, 'Invalid Username')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'username or password doesn\'t exist')

        return render(request, self.template_name, {})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

    # def post(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {})


class CreateListingView(View):
    template_name = 'create-listing.html'

    def get(self, request, *args, **kwargs):
        form = ListingForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, self.template_name, {})


class UpdateListingView(View):
    template_name = 'update-listing.html'

    def get(self, request, pk, *args, **kwargs):
        listing = Listing.objects.get(id=pk)
        form = ListingForm(instance=listing)
        return render(request, self.template_name, {'form':form})

    def post(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            listing = Listing.objects.get(id=pk)
            form = ListingForm(request.POST, request.FILES, instance=listing)
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, self.template_name, {})


class DeleteListingView(View):
    template_name = 'delete-listing.html'

    def get(self, request, pk, *args, **kwargs):
        listing = Listing.objects.get(id=pk)
        return render(request, self.template_name, {'listing':listing})

    def post(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            listing = Listing.objects.get(id=pk)
            if request.method == 'POST':
                listing.delete()
                return redirect('home')
        return render(request, self.template_name, {})


class ListingChartView(View):
    template_name = 'listing-chart.html'

    def get(self, request, *args, **kwargs):
        listing_count = Listing.objects.values(year=ExtractYear('created'), month=ExtractMonth('created')).annotate(total=Count('id'))
        labels = []
        items = []
        for item in listing_count:
            labels.append("{0}-{1}".format(item['year'], item['month']))
            items.append(item['total'])
        return render(request, self.template_name, {'labels':labels, 'items':items})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = RegisterForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user.password = make_password(password)
                user.save()
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Account Created for {username} & Logged In!')
                return redirect('home')
        else:
            form = RegisterForm()
        return render(request, self.template_name, {'form':form})