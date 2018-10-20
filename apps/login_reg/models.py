from django.db import models
from django.core.validators import EmailValidator
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, regData):
        errors = {}

        # Check the first name input
        if 'fName' in regData:
            if len(regData['fName']) < 1:
                errors['fName'] = "Please enter your first name"
            elif len(regData['fName']) < 3:
                errors['fName'] = "First name should be at least 3 characters"
            elif not regData['fName'].isalpha():
                errors['fName'] = "First name should only contain alphabetical characters"

        # Check the last name input
        if 'lName' in regData:
            if len(regData['lName']) < 1:
                errors['lName'] = "Please enter your last name"
            elif len(regData['lName']) < 3:
                errors['lName'] = "Last name should be at least 3 characters"
            elif not regData['lName'].isalpha():
                errors['lName'] = "Last name should only contain alphabetical characters"

        # Check email address input
        if 'email' in regData:
            if len(regData['email']) < 1:
                errors['email'] = "Please enter your email address"
            else:
                eValidator = EmailValidator()
                try:
                    eValidator(regData['email'])
                except:
                    errors['email'] = "Please enter a valid email address"
            
            if 'email' not in errors:
                try:
                    if User.objects.get(email=regData['email']):
                        errors['email'] = "Email address already taken"
                except:
                    print("No query")
        
        # Check password input
        if 'password' in regData:
            if len(regData['password']) < 1:
                errors['password'] = "Please enter a password"
            elif len(regData['password']) < 8:
                errors['password'] = "Password must be between 8-20 characters long"
            elif len(regData['password']) > 20:
                errors['password'] = "Password must be between 8-20 characters long"
        
        # Check password confirm input
        if 'pwConfirm' in regData:
            if len(regData['pw_confirm']) < 1:
                errors['pwConfirm'] = "Please confirm your password"
            elif regData['password'] != regData['pw_confirm']:
                errors['password'] = "Passwords do not match"
                errors['pwConfirm'] = "Passwords do not match"
        
        return errors
    
    def login_validator(self, loginData):
        errors = {}

        # Check email address input
        if 'emailL' in loginData:
            if len(loginData['emailL']) < 1:
                errors['emailL'] = "Please enter your email address"
            else:
                eValidator = EmailValidator()
                try:
                    eValidator(loginData['emailL'])
                except:
                    errors['emailL'] = "Please enter a valid email address"
            
            if 'emailL' not in errors:
                try:
                    if User.objects.get(email=loginData['emailL']):
                        print("Successfully found 1 user")
                except:
                    errors['emailL'] = "Email address entered was not found, please register"
        
        if len(errors):
            return errors
        
        # Check password input
        if 'passwordL' in loginData:
            if len(loginData['passwordL']) < 1:
                errors['passwordL'] = "Please enter your password"
            
            if 'passwordL' not in errors:
                user = User.objects.get(email=loginData['emailL'])
                try:
                    if not bcrypt.checkpw(loginData['passwordL'].encode(), user.password.encode()):
                        erros['passwordL'] = "Password entered was incorrect"
                except:
                    print("Secrecy issue")                        

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    objects = UserManager()

