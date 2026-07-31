from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

User = get_user_model()


def blacklist_all_tokens(user: User):
    tokens = OutstandingToken.objects.filter(user=user).exclude(blacklistedtoken__isnull=False)
    BlacklistedToken.objects.bulk_create([BlacklistedToken(token=t) for t in tokens], ignore_conflicts=True)
