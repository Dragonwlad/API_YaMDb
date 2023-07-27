from rest_framework import serializers

from users.models import User


class AdmineCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',
                  ]
        model = User
        read_only_fields = ('confirmation_code',)


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  ]
        model = User
        read_only_fields = ('confirmation_code',)
