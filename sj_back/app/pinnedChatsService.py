from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PinnedChat, User, Chat
from .serializers import PinnedChatSerializer


@api_view(['GET'])
def get_pinned_chats(request, user_id):
    """Get all pinned chats for a specific user"""
    try:
        pinned_chats = PinnedChat.objects.filter(user_id=user_id)
        serializer = PinnedChatSerializer(pinned_chats, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_pinned_chat(request):
    """Create a new pinned chat"""
    try:
        serializer = PinnedChatSerializer(data=request.data)
        if serializer.is_valid():
            # Check if user already has 3 pinned chats
            user_id = request.data.get('user')
            existing_pins = PinnedChat.objects.filter(user_id=user_id).count()

            if existing_pins >= 3:
                return Response(
                    {"error": "User can only pin up to 3 chats. Unpin one first."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if this chat is already pinned
            chat_id = request.data.get('chat')
            if PinnedChat.objects.filter(user_id=user_id, chat_id=chat_id).exists():
                return Response(
                    {"error": "This chat is already pinned."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_pinned_chat(request, user_id, chat_id):
    """Delete a pinned chat"""
    try:
        pinned_chat = PinnedChat.objects.filter(user_id=user_id, chat_id=chat_id).first()
        if pinned_chat:
            pinned_chat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Pinned chat not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)