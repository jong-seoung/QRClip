from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from accounts.models import User, Profile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields="__all__"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user_by_email = User.objects.get(email=data['email'])

            if user_by_email.check_password(data['password']):
                update_last_login(None, user_by_email)
                return user_by_email
            else:
                raise serializers.ValidationError("회원 정보가 잘못되었습니다.")
        except User.DoesNotExist:
            raise serializers.ValidationError("회원 정보가 잘못되었습니다.")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"
        read_only_fields = ['user']