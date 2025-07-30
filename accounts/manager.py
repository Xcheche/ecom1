from django.contrib.auth.models import BaseUserManager

#Creating user
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_name, password=None): # Can add phone number if desired
        if not email:
            raise ValueError("Users must have an email address")
        if not user_name:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email), #Turns cap input to small
            first_name=first_name,
            last_name=last_name,
            user_name=user_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
# Creating the superuser
    def create_superuser(self, email, first_name, last_name, user_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            password=password
        )
        # giving permissions to the superuser
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user