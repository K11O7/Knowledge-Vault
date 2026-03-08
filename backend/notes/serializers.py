from rest_framework import serializers
from .models import Note
from tags.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class NoteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    tag_details = TagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "tags",
            "tag_details",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        user =  validated_data.pop("user")
        note = Note.objects.create(user=user, **validated_data)

        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            note.tags.add(tag)

        return note