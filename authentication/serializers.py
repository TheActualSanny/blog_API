from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length = 128)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')

    def validate(self, attrs):
        '''
            We check if the passed password values are equal.
            If they are not, we will raise a ValidationError in views.py
        '''

        if attrs.get('password') != attrs.get('password_confirm'):
            raise ValidationError('The passwords must match!') 
        try:
            User.objects.get(username = 'username')
            raise ValueError('User already exists, choose a different username!')
        except User.DoesNotExist:
            return attrs
            