from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from authz.permissions import HasAdminPermission
from messages_api.models import Message
from messages_api.serializers import MessageSerializer

class MessageApiView(RetrieveAPIView):
    serializer_class = MessageSerializer
    text = None

    def get_object(self):
        return Message(text=self.text)


class PublicMessageApiView(MessageApiView):
    text = "The API doesn't require an access token to share this message."


class ProtectedMessageApiView(MessageApiView):
    text = "The API successfully validated your access token."
    permission_classes = [IsAuthenticated]


class AdminMessageApiView(MessageApiView):
    text = "The API successfully recognized you as an admin."
    permission_classes = [IsAuthenticated, HasAdminPermission]
