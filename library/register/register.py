from rest_framework.authtoken.models import Token

from accounts.models import User
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from core.settings import KAFKA_LOGIN_TOPIC, SIGNUP_KAFKA_TOPIC
from library.Kafka.kafka_connect import KafkaConnect


def send_user_signin_email(user):
    email = user.email
    messages = [{
        "email": email
    }]
    KafkaConnect.write_data_to_kafka(KAFKA_LOGIN_TOPIC, messages)


def send_user_sign_up_email(user):
    email = user.email
    messages = [{
        "email": email
    }]
    KafkaConnect.write_data_to_kafka(SIGNUP_KAFKA_TOPIC, messages)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = User.objects.get(email=email)
            registered_user.check_password(settings.SOCIAL_SECRET)
            send_user_signin_email(registered_user)
            Token.objects.filter(user=registered_user).delete()
            Token.objects.create(user=registered_user)
            new_token = list(Token.objects.filter(
                user_id=registered_user).values("key"))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': str(new_token[0]['key'])}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': email, 'email': email,
            'password': settings.SOCIAL_SECRET
        }
        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        new_user = User.objects.get(email=email)
        new_user.check_password(settings.SOCIAL_SECRET)
        send_user_sign_up_email(new_user)
        Token.objects.create(user=new_user)
        new_token = list(Token.objects.filter(user_id=new_user).values("key"))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': str(new_token[0]['key']),
        }
