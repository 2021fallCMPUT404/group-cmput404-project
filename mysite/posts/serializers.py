from rest_framework import serializers
from .models import Post, Comment, Like


class PostSerializer(serializers.ModelSerializer):
    '''
    PUBLIC = 0
    PRIVATE = 1
    # FREINDS=2    #Need friend system?

    Privacy = (
        (PUBLIC, "PUBLIC"),
        (PRIVATE, "PRIVATE"),  #only shows to me
        #(FREINDS,"FRIENDS"),
        #(Unlisted,"Unlisted")
    )

    type = 'post'
    title = serializers.CharField(default='New Post!', max_length=200)
    text = serializers.CharField()
    image = serializers.ImageField()
    pub_date = serializers.DateTimeField()
    author = serializers.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = serializers.ForeignKey(User,
                                         on_delete=models.CASCADE,
                                         related_name='+')

    shared_on = serializers.DateTimeField()
    privacy = serializers.IntegerField(choices=Privacy, default=PUBLIC)
    visible = None

    contentType = serializers.CharField(default="text/plain")
    '''
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.author = validated_data.get('author', instance.author)
        instance.shared_user = validated_data.get('shared_user',
                                                  instance.shared_user)
        instance.shared_on = validated_data.get('shared_on',
                                                instance.shared_on)
        instance.privacy = validated_data.get('privacy', instance.privacy)
        instance.contentType = validated_data.get('contentType',
                                                  instance.contentType)
        instance.save()
        return instance