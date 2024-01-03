# Project name --> knowYourCaller

# Desciption -- > KnowYourCaller

            Registration and Profile:
                        ● A user has to register with at least name and phone number, along with a password, before
                        using. He can optionally add an email address.
                        ● Only one user can register on the app with a particular phone number.
                        ● A user needs to be logged in to do anything; there is no public access to anything.
                        ● You can assume that the user’s phone contacts will be automatically imported into the app’s
                        database - you don’t need to implement importing the contacts.
                        Spam:
                        ● A user should be able to mark a number as spam so that other users can identify spammers via
                        the global database. Note that the number may or may not belong to any registered user or
                        contact - it could be a random number.
                        Search:
                        ● A user can search for a person by name in the global database. Search results display the name,
                        phone number and spam likelihood for each result matching that name completely or partially.
                        Results should first show people whose names start with the search query, and then people
                        whose names contain but don’t start with the search query.
                        ● A user can search for a person by phone number in the global database. If there is a registered
                        user with that phone number, show only that result. Otherwise, show all results matching that
                        phone number completely - note that there can be multiple names for a particular phone number
                        in the global database, since contact books of multiple registered users may have different names
                        for the same phone number.
                        ● Clicking a search result displays all the details for that person along with the spam likelihood. But
                        the person’s email is only displayed if the person is a registered user and the user who is
                        searching is in the person’s contact list.
                        Data Population:
                        ● For your testing you should write a script or other facility that will populate your database with a
                        decent amount of random, sample data.


            <!-- KnowYourCaller is a Django-based web application that provides a REST API to be
            consumed by a mobile app. The app allows users to check if a phone number is marked
            as spam and provides a search feature to find a person's name by entering their phone
            number. Users can register, mark numbers as spam, and search the global database for
            contact information. The project emphasizes performance, security, and seamless
            integration with a mobile app's front end. --!>
            
            Features -->
                User registration with optional email address
                Marking phone numbers as spam
                Global database search by name or phone number
                Displaying contact information, spam likelihood,
                and email (if in contact list)



### Prerequisites

- Python (3.7 or higher)
- Django (3.x)

### Getting started

Apply Migrations --> run the command --> python manage.py makemigrations
                                     --> python mange.py migrate

Run the development server: --> python manage.py runserver


Data Population --> command --> python manage.py populate_data

### Now you can go to localhost:8000/admin or your default localhost:8080/admin --> and now you can do the crud operations as your wish


### superuser just in case --> admin@admin.com, username - admin, password - admin
