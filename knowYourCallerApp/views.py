from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import CustomUser, PhoneNumber, SpamAction, UserContact
from django.contrib import messages
from django.urls import reverse



def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return render(request, 'knowYourCallerApp/index.html')
            


#  A user has to register with at least name and phone number, along with a password, before
# using. He can optionally add an email address.

def signUpUser(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]

        number_exist = CustomUser.objects.filter(phone_number=phone).first()
        if number_exist is not None:
            print("User exist with same phone number!")
            context = {
                "msg": "User exist with same phone number, Try with a different one."
            }
            return render(request, 'knowYourCallerApp/signup.html', context)
        else:
            user = CustomUser.objects.create_user(name = name, phone_number = phone, email = email, password = password)
            user.save()
            print("user created successfully.")
            messages.success(request, 'User successfully created. Please Sign in.')

            return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'knowYourCallerApp/signup.html')
    



def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            print("user logged in successfully.")
            return redirect('/')
        else:
            context = {
                "message": "Please try again with correct credentials!"
            }
            print("please try again.")
            return render(request, 'knowYourCallerApp/login.html', context)
    login_message = messages.get_messages(request)
    context = {'login_message': login_message}
    return render(request, 'knowYourCallerApp/login.html', context)



def logoutUser(request):
    logout(request)
    print("logged out successfully.")
    messages.success(request, 'You are logged out successfully!')
    return HttpResponseRedirect(reverse('login'))





def mark_as_spam(request, query):
    if request.user.is_authenticated:
        try:
            # Check if the user has already performed the action
            user = request.user
            # Create PhoneNumber instance if it does not exist
            phoneNumber_instance, created = PhoneNumber.objects.get_or_create(number = query)

            spam_action, created = SpamAction.objects.get_or_create(user=user, phone_number=phoneNumber_instance)
            if not spam_action.is_marked_as_spam:
                # Mark the action as performed by the user
                spam_action.is_marked_as_spam = True
                spam_action.save()

            # get the PhoneNumber instance
            number_object = PhoneNumber.objects.get(number = query)

            # Update the spam_likelihood
            number_object.spam_likelihood += 1
            number_object.save()

            return HttpResponse("phone number is marked as spam!")
        
        # if multiple phone number entries returned
        except PhoneNumber.MultipleObjectsReturned:
            most_spammed_number = PhoneNumber.objects.filter(number = query).order_by('-spam_likelihood').first()
            most_spammed_number.spam_likelihood += 1
            most_spammed_number.save()

            return HttpResponse("Found more than one phone number entries. marked most_spammed one as spam")
        
    else:
        return redirect('/login')



def search_person_by_name(request, query):
    try:
        print(query)
        starts_with_results = PhoneNumber.objects.filter(Q(name__startswith=query)).values()
        contains_with_results = PhoneNumber.objects.filter(Q(name__icontains=query)).values().exclude(name__istartswith=query)
        print(starts_with_results)
        print(contains_with_results)

        # results = starts_with_results + contains_with_results
        results = list(starts_with_results) + list(contains_with_results)
        print(results)
        search_results = []
        for result in results:
            result_info = {
                'name': result['name'],
                'phone_number': result['number'],
                'spam_likelihood': result['spam_likelihood'],
            }
            search_results.append(result_info)

        return JsonResponse({'results': search_results})

    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    



def search_person_by_number(request, query):
    print(query)
    try:
        if query.isdigit() and len(query) >= 10:
            # check if the number is registered as user
            registered_user = CustomUser.objects.get(phone_number = query)
            print(registered_user)

            # find person's contact list and then check if the request.user exists in the person's contact list
            is_contact = UserContact.objects.filter(user=registered_user, phone_number = request.user.phone_number).exists()

            # find that particular phone number in the global database which is mostly spammed.
            most_spammed = PhoneNumber.objects.filter(number=query).order_by('-spam_likelihood').first()
            # print(most_spammed.spam_likelihood)

            result_info = {
                'name': registered_user.name,
                'phone_number': registered_user.phone_number,
                # I (registered user) will get the email information of the person for which I am searching for only when the person has my number saved in his/her contact list
                'email': registered_user.email if is_contact else None,
                'spam_likelihood': most_spammed.spam_likelihood
            }

            return JsonResponse({'result': result_info})

        else:
            return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    except CustomUser.DoesNotExist :
        print("custom user does not exist.")
        results = PhoneNumber.objects.filter(number=query)

        search_results = []
        for result in results:
            result_info = {
                'name': result.name,
                'phone_number': result.number,
                'spam_likelihood': result.spam_likelihood,
            }
            search_results.append(result_info)

        return JsonResponse({'results': search_results})

    except Exception as e:
        print("manual exception is throwing.")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    






    