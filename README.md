# Project name --> knowYourCaller

# Desciption -- > KnowYourCaller

            <!-- KnowYourCaller is a Django-based web application that provides a REST API to be consumed by a mobile app. The app allows users to check if a phone number is marked as spam and provides a search feature to find a person's name by entering their phone number. Users can register, mark numbers as spam, and search the global database for contact information. The project emphasizes performance, security, and seamless integration with a mobile app's front end.
            
            Features -->
                User registration with optional email address
                Marking phone numbers as spam
                Global database search by name or phone number
                Displaying contact information, spam likelihood, and email (if in contact list)



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