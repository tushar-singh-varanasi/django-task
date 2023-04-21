from django.shortcuts import render
from rest_framework.response import Response
from .serializers import (UserSerilizer ,Userloginserilaizer,StudentSerilizer,TeacherSerilizer,UserChangepasswordSerilizer,
                          SendPasswordResetserializer,UserPasswordReseSerializer)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#teacher signup class
class TeacherResgistratipn(APIView):
    def post(self, request, format=None):
        serializer = UserSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        student_group,create= Group.objects.get_or_create(name='Teacher')
        student_group.user_set.add(user)
        token=get_token_for_user(user)
        return Response({'token':token,'msg':'Registration Successfuly'},status=status.HTTP_201_CREATED
                        )


class UserLogin(APIView):
    def post(self,request,format=None):
        Serilizer=Userloginserilaizer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        email=Serilizer.data.get('email')
        password=Serilizer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            token=get_token_for_user(user)
            return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_error':['Email or password not match']}},status=status.HTTP_400_BAD_REQUEST)
        
#in this class only teacher is authenticated for add student and see the students list
class StudentResgistratipn(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        if request.user.groups.filter(name='Teacher').exists():
            serializer = UserSerilizer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student_data=serializer.save()
            student_group,create= Group.objects.get_or_create(name='Student')
            print(student_group)
            student_group.user_set.add(student_data)
           
            token=get_token_for_user(student_data)
            return Response({'token':token,'msg':'Registration Successfuly'},status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'Registration unSuccessfuly'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get(self, request, format=None):
        if request.user.groups.filter(name='Teacher').exists() :
           
            snippets = User.objects.filter(groups__name='Student')
            serializer = StudentSerilizer(snippets, many=True)
            return Response(serializer.data)
      
        else:
            return Response({'msg':'method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
# in this class Students see his information only
class StudentProfile(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        if request.user.groups.filter(name='Student').exists() :
            snippets=User.objects.filter(email=request.user)
            Serilizer=StudentSerilizer(snippets,many=True)
            
            return Response(Serilizer.data)
        else:
            return Response({'msg':'method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#  in this class admin is able to add  and see the  teacher list

class AdminAddTeacher(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    def post(self, request, format=None):
        serializer = UserSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        student_group,create= Group.objects.get_or_create(name='Teacher')
        student_group.user_set.add(user)
        token=get_token_for_user(user)
        return Response({'token':token,'msg':'Registration Successfuly'},status=status.HTTP_201_CREATED
                        )
    def get(self, request, format=None):
        snippets = User.objects.filter(groups__name='Teacher')
        serializer = TeacherSerilizer(snippets, many=True)
        return Response(serializer.data)
        
#  in this class admin is able to add  and see the  student list
class AdminAddStudent(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    def post(self, request, format=None):
        serializer = UserSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        student_group,create= Group.objects.get_or_create(name='Student')
        student_group.user_set.add(user)
        token=get_token_for_user(user)
        return Response({'token':token,'msg':'Registration Successfuly'},status=status.HTTP_201_CREATED
                        )
    def get(self, request, format=None):
        snippets = User.objects.filter(groups__name='Student')
        serializer = TeacherSerilizer(snippets, many=True)
        return Response(serializer.data)


class UserChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        Serilizer=UserChangepasswordSerilizer(data=request.data, context={'user':request.user})
       
        if Serilizer.is_valid(raise_exception=True):
            return Response({'msg':'password change successfuly'},status.HTTP_200_OK)
        return Response(Serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmail(APIView):
    def post(self,request,format=None):
        Serilizer=SendPasswordResetserializer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        return Response({'msg':'password resent link send please check your email'},status=status.HTTP_200_OK)

class UserPasswordReset(APIView):
     def post(self,request,uid,token,format=None):
        Serilizer=UserPasswordReseSerializer(data=request.data,context={'uid':uid,'token':token})
        Serilizer.is_valid(raise_exception=True)
        return Response({'msg':'password reset successfully'},status=status.HTTP_200_OK)

 




   
