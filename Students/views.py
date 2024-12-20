# from rest_framework import viewsets
# from .models import Students
# from .serializers import StudentsSerializer
# # from rest_framework import permissions
# # from rest_framework.decorators import action
# # from rest_framework.response import Response

# # class StudentsViewSet(viewsets.ModelViewSet):
# #     permission_classes = [permissions.AllowAny]
# #     queryset = StudentsViewSet.objects.all()
# #     serializer_class = StudentsSerializer
    
# #     @action(detail=False, methods=['GET', url_path='all_students'])
# #     def all_students(self, request):
# #         objs = self.get_queryset()
# #         if objs:
# #             serializer  =self.get_serializer(objs)
# #             return Response(serializer.data)
# #         else:
# #             return Response({'error': 'No students found.'}, status=status.HTTP_404_NOT_FOUND)



# from rest_framework import generics


# class StudentAPIView(generics.ListCreateAPIView):
#     serializer_class = StudentsSerializer
#     queryset = Students.objects.all()

# class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = StudentsSerializer
#     queryset = Students.objects.all()



from rest_framework import generics
from .models import Students, Attendance, Payment
from .serializers import StudentsSerializer, AttendanceSerializer, PaymentSerializer

class StudentAPIView(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

class MarkAttendanceAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        student = Students.objects.get(pk=student_id)
        serializer.save(student=student)

class MakePaymentAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        student = Students.objects.get(pk=student_id)
        serializer.save(student=student)
