from django.contrib.auth.models import BaseUserManager


# CUSTOM USER MANAGER
class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, tc, password=None, confirm_password=None
    ):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email, password=password, first_name=first_name, last_name=last_name, tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
