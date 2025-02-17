from django.contrib.auth.models import User
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KeycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):
	def create_user(self, claims):
		user = User.objects.create_user(
			username=claims['email'],
			email=claims['email'],
			first_name=claims['given_name'],
			last_name=claims['family_name'],
			is_active=claims['email_verified'],
		)
		return user

	def update_user(self, user, claims):
		user.email = claims.get('email', user.email)
		user.username = claims.get('email', user.username)
		user.first_name = claims.get('given_name', user.first_name)
		user.last_name = claims.get('family_name', user.last_name)
		user.save()
		return user

	def store_tokens(self, access_token, id_token):
		super().store_tokens(access_token, id_token)
		print(access_token)
		print()
		print(id_token)
