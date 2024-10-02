"""Function tests for the `/users/researchgroups/` endpoint."""

from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from tests.utils import CustomAsserts


class EndpointPermissions(APITestCase, CustomAsserts):
    """Test endpoint user permissions.

    Endpoint permissions are tested against the following matrix of HTTP responses.

    | Authentication              | GET | HEAD | OPTIONS | POST | PUT | PATCH | DELETE | TRACE |
    |-----------------------------|-----|------|---------|------|-----|-------|--------|-------|
    | Anonymous user              | 401 | 401  | 401     | 401  | 401 | 401   | 401    | 401   |
    | Authenticated user          | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 403   |
    | Staff user                  | 200 | 200  | 200     | 201  | 405 | 405   | 405    | 405   |
    """

    endpoint = '/users/researchgroups/'
    fixtures = ['multi_research_group.yaml']

    def test_anonymous_user_permissions(self) -> None:
        """Test unauthenticated users are returned a 401 status code for all request types."""

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_401_UNAUTHORIZED,
            head=status.HTTP_401_UNAUTHORIZED,
            options=status.HTTP_401_UNAUTHORIZED,
            post=status.HTTP_401_UNAUTHORIZED,
            put=status.HTTP_401_UNAUTHORIZED,
            patch=status.HTTP_401_UNAUTHORIZED,
            delete=status.HTTP_401_UNAUTHORIZED,
            trace=status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_permissions(self) -> None:
        """Test general authenticated users can create new research groups."""

        user = User.objects.get(username='generic_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_403_FORBIDDEN,
            post_body={'name': 'Group FooBar', 'pi': 1}
        )

    def test_staff_user_permissions(self) -> None:
        """Test staff users have full read and write permissions."""

        user = User.objects.get(username='staff_user')
        self.client.force_authenticate(user=user)

        self.assert_http_responses(
            self.endpoint,
            get=status.HTTP_200_OK,
            head=status.HTTP_200_OK,
            options=status.HTTP_200_OK,
            post=status.HTTP_201_CREATED,
            put=status.HTTP_405_METHOD_NOT_ALLOWED,
            patch=status.HTTP_405_METHOD_NOT_ALLOWED,
            delete=status.HTTP_405_METHOD_NOT_ALLOWED,
            trace=status.HTTP_405_METHOD_NOT_ALLOWED,
            post_body={'name': 'Research Group 3', 'pi': 1},
        )
