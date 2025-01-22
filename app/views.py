from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Content
from app.serializers import UserRegistrationSerializer, UserLoginSerializer, ContentSerializer, ContentDetailsSerializer


# Create your views here.
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "message": "User registered successfully"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": {"message": serializer.errors}},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                token = serializer.validated_data["token"]
                if token:
                    return Response({"success": True, "message": "Login successful", "data": {"token": token.key}},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({"success": False, "error": {"message": "Invalid credentials"}},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"success": False, "error": {"message": serializer.errors}},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.role.name == "Admin":
                contents = Content.objects.all()
            elif request.user.role.name == "Author":
                contents = Content.objects.filter(user=request.user)
            else:
                return Response({"success": False, "error": {"message": "Unauthorized"}},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = ContentDetailsSerializer(contents, many=True)
            return Response({"success": True, "message": "Contents retrieved successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            if request.user.role.name != "Author":
                return Response({"success": False, "error": {"message": "Only authors can create content."}},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = ContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"success": True, "message": "Content created successfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": {"message": serializer.errors}},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            content = self.get_object(pk)
            if not content:
                return Response({"success": False, "error": {"message": "Content not found"}},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.user.role.name == "Admin" or (request.user.role.name == "Author" and
                                                     content.user == request.user):
                serializer = ContentDetailsSerializer(content)
                return Response({"success": True, "message": "Contents retrieved successfully",
                                 "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": {"message": "Unauthorized"}},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            content = self.get_object(pk)
            if not content:
                return Response({"success": False, "error": {"message": "Content not found"}},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.user.role.name == "Admin" or (request.user.role.name == "Author" and
                                                     content.user == request.user):
                serializer = ContentSerializer(content, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success": True, "message": "Content edited successfully"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"success": False, "error": {"message": serializer.errors}},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"success": False, "error": {"message": "Unauthorized"}},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            content = self.get_object(pk)
            if not content:
                return Response({"success": False, "error": {"message": "Content not found"}},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.user.role.name == "Admin" or (request.user.role.name == "Author" and
                                                     content.user == request.user):
                content.delete()
                return Response({"success": True, "message": "Content deleted successfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": {"message": "Unauthorized"}},
                                status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            search_term = request.query_params.get('search', None)

            if request.user.role.name == "Admin":
                content_results = Content.objects.filter(
                    Q(title__icontains=search_term) |
                    Q(body__icontains=search_term) |
                    Q(summary__icontains=search_term) |
                    Q(contentcategory__category__name__icontains=search_term)
                ).distinct()
            elif request.user.role.name == "Author":
                content_results = Content.objects.filter(
                    Q(title__icontains=search_term) |
                    Q(body__icontains=search_term) |
                    Q(summary__icontains=search_term) |
                    Q(contentcategory__category__name__icontains=search_term),
                    user=request.user,
                ).distinct()
            else:
                return Response({"success": False, "error": {"message": "Unauthorized"}},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = ContentDetailsSerializer(content_results, many=True)
            return Response({"success": True, "message": "Contents retrieved successfully",
                             "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "error": {"message": str(e)}},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
