from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentification.models import CustomUser
from rest_framework import status
from users.serilizers import UserListSerializers
# Create your views here.
class AdditionDetailsTeacher(APIView):
    def post(self,request):
        print('ooooo')
        try:
            print('888888888888888888')
            id=request.data.get('user_id')
            print(id)
            user=CustomUser.objects.get(pk=id)
            print(user)
            phone=request.data.get('phone')
            qualification=request.data.get('qualification')
            bank_account=request.data.get('bankaccount')
            ifsc=request.data.get('ifsc')
            id_proof=request.data.get('idproof')
            certificate=request.data.get('certificate')
            
            errors=[]

            # Basic validations
            if not phone or not phone.strip():
                errors.append('Phone number is required')
            # Add more validations for phone number format if needed

            if not qualification or not qualification.strip():
                errors.append('Qualification is required')

            if not bank_account or not bank_account.strip():
                errors.append('Bank account number is required')

            if not ifsc or not ifsc.strip():
                errors.append('IFSC code is required')
            # Add IFSC format validation using a regular expression if needed

            if not id_proof:
                errors.append('ID proof file is required')

            if not certificate:
                errors.append('Certificate file is required')

            # If there are errors, return them as a JSON response
            if errors:
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            
            print('===================')
            if user:
                user.phone = phone
                user.qualification = qualification
                user.bank_account_number = bank_account
                user.ifsc_code = ifsc
                user.id_proof = id_proof
                user.certificate = certificate
                user.teacher_request = True
                try:
                    print('Before save')
                    user.save()
                    print('After save')
                    print('Data Submission Successfully')
                except Exception as e:
                    print(f'Error during save: {e}')
                    return Response({'errors': 'Error during save'}, status=status.HTTP_400_BAD_REQUEST)
                serializer = UserListSerializers(user)
                return Response({'teacher': serializer.data, 'message': 'Data Submission Successfully'},status=status.HTTP_200_OK)
            else:
                print('User not found')
                return Response({'errors': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({'errors': 'somthing problems'}, status=status.HTTP_400_BAD_REQUEST)

