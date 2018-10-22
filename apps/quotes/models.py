from django.db import models
from django.core.validators import EmailValidator
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, regData, id=0, update=False):
        errors = {}

        # Remove spaces from names
        fName = regData['fName'].replace(' ', '')
        lName = regData['lName'].replace(' ', '')

        # If we're doing an update, get an instane of the current user
        if update:
            user = User.objects.get(id=id)

        # Check the first name input
        if 'fName' in regData:
            if len(fName) < 1:
                errors['fName'] = "Please enter your first name"
            elif len(fName) < 3:
                errors['fName'] = "First name should be at least 3 characters"
            elif not fName.isalpha():
                errors['fName'] = "First name should only contain alphabetical characters"

        # Check the last name input
        if 'lName' in regData:
            if len(lName) < 1:
                errors['lName'] = "Please enter your last name"
            elif len(lName) < 3:
                errors['lName'] = "Last name should be at least 3 characters"
            elif not lName.isalpha():
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
                        if update:
                            if regData['email'] != user.email:
                                print("Is it even coming here?")
                                errors['email'] = "Email address already taken"
                        else:
                            errors['email'] = "Email address already taken"
                except:
                    print("Invalid query")
        
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

class QuoteManager(models.Manager):
    def quote_validator(self, quoteData):
        errors = {}

        # Remove spaces from name
        nameV = quoteData['author'].replace(' ', '')
        # Remove decimals from name
        nameV = nameV.replace('.', '')

        # Check the author's name input
        if 'author' in quoteData:
            if len(nameV) < 1:
                errors['author'] = "Please enter the author's name"
            elif len(nameV) < 4:
                errors['author'] = "Author's name should be at least 4 characters"
            elif not nameV.isalpha():
                errors['author'] = "Auhtor's name should only contain alphabetical characters"

        # Check the quote content input
        if 'content' in quoteData:
            if len(quoteData['content']) < 1:
                errors['content'] = "Please enter the quote"
            elif len(quoteData['content']) < 4:
                errors['content'] = "Quote should be at least 4 characters"
        
        return errors

class LikeManager(models.Manager):
    def like_validator(self, quote, liker):
        errors = {}

        # Check if the liker has already liked this quote before
        likes = Like.objects.filter(quote=quote)
        # print("Over here", likes)
        for like in likes:
            if like.user == liker:
                errors['liker'] = "Already liked"
        
        return errors

    def count_likes(self, quote):

        count = 0
        likes = Like.objects.filter(quote=quote)
        for like in likes:
            count += 1
        
        return count

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=45)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quotes")
    objects = QuoteManager()

class Like(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="likes")
    objects = LikeManager()
