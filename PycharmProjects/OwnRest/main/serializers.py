from rest_framework import serializers

from . models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'price', 'title', 'category', 'created_at', 'text',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['likes'] = len(LikeSerializer(instance.likes.all(), many=True).data)
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = PostImageSerializer(instance.images.all(), many=True,
                                                       context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        images = request.FILES
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        for image in images.getlist('image'):
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('image'):
            PostImage.objects.create(post=instance, image=image)
        return instance


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url=request.build_absolute_uri(url)
                print(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['image']=self._get_image_url(instance)
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('user')
            fields.pop('like')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')
        like = Like.objects.get_or_create(user=user, post=post)[0]
        like.like = True if like.like is False else False
        like.save()
        return like

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class ParsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    link = serializers.CharField(max_length=255)

