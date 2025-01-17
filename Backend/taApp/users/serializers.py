from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import ProfessorProfile, StudentProfile
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class ProfessorRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = ProfessorProfile
        fields = ['user', 'national_no', 'password2']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists!")
        return username

    def validate(self, data):
        if data['user']['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        national_no = validated_data.pop('national_no')
        prof = ProfessorProfile.objects.create(user=user, national_no=national_no)
        return prof

class ProfessorLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), **data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class StudentRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = StudentProfile
        fields = ['user', 'stu_no', "phone_no" , 'is_ta' , 'password2']

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists!")
        return username

    def validate(self, data):
        if data['user']['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        stu_no = validated_data.pop('stu_no')
        phone_no = validated_data.pop('phone_no')
        is_ta = validated_data.pop('is_ta')
        stu = StudentProfile.objects.create(user=user, stu_no=stu_no, is_ta=is_ta, phone_no=phone_no)
        return stu

class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(request=self.context.get('request'), **data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")