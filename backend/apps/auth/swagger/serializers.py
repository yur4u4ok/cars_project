from apps.users.serializers import UserSerializer


class SwaggerUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'email', 'last_login', 'is_superuser', 'is_active', 'is_staff',
                  'created_at', 'updated_at', 'profile'
                  )
