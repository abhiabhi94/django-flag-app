from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.username) + six.text_type(timestamp) + six.text_type(user.is_active)


account_activation_token = TokenGenerator()
