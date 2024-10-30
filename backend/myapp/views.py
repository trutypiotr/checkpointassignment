from rest_framework import serializers, generics
from slack_sdk.errors import SlackApiError

from .models import Pattern, CaughtMessage
from .slack import slack_client


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = "__all__"


class CaughtMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaughtMessage
        fields = "__all__"


class PatternListView(generics.ListAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer


class CaughtMessageCreateView(generics.CreateAPIView):
    queryset = CaughtMessage.objects.all()
    serializer_class = CaughtMessageSerializer

    def perform_create(self, serializer):
        caught_message = serializer.save()
        try:
            slack_client.chat_update(
                channel=caught_message.channel,
                ts=str(caught_message.ts),
                text="Original message has been blocked",
            )
        except SlackApiError as e:
            print(f"Error updating message on slack: {e}")
