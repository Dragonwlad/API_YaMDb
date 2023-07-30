from rest_framework import serializers

from users.models import User


class AdminCreateUserSerializer(serializers.ModelSerializer):

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
                  ]
        model = User
        read_only_fields = ('confirmation_code',)


class UserPathSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  ]
        model = User
        read_only_fields = ('confirmation_code',)
