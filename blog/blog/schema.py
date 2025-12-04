import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from posts.models import Category, Topic, Post


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "description")


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = ("id", "name", "category", "created")


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "text",
            "topic",
            "slug",
            "created_at",
            "created_by",
            "updated_at",

        )

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")




class Query(graphene.ObjectType):

    all_categories = graphene.List(CategoryType)
    all_topics = graphene.List(TopicType)
    all_posts = graphene.List(PostType)


    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))
    topic_by_id = graphene.Field(TopicType, id=graphene.Int(required=True))
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))


    categories_by_name_contains = graphene.List(
        CategoryType,
        substr=graphene.String(required=True),
    )


    posts_count_by_user = graphene.Int(
        username=graphene.String(required=True),
    )


    posts_by_category_name = graphene.List(
        PostType,
        category_name=graphene.String(required=True),
    )

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_topics(root, info):
        return Topic.objects.select_related("category").all()

    def resolve_all_posts(root, info):
        return Post.objects.select_related("topic", "topic__category", "created_by").all()

    def resolve_category_by_id(root, info, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return None

    def resolve_topic_by_id(root, info, id):
        try:
            return Topic.objects.get(pk=id)
        except Topic.DoesNotExist:
            return None

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None


    def resolve_categories_by_name_contains(root, info, substr):
        return Category.objects.filter(name__icontains=substr)

    def resolve_posts_count_by_user(root, info, username):
        return Post.objects.filter(created_by__username=username).count()

    def resolve_posts_by_category_name(root, info, category_name):
        return Post.objects.filter(topic__category__name__iexact=category_name)



class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        topic_id = graphene.Int(required=True)
        slug = graphene.String(required=True)
        created_by_id = graphene.Int(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, title, text, topic_id, slug, created_by_id):
        from django.contrib.auth.models import User
        try:
            topic = Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            raise Exception("Invalid topic_id")

        try:
            user = User.objects.get(pk=created_by_id)
        except User.DoesNotExist:
            raise Exception("Invalid created_by_id")

        post = Post.objects.create(
            title=title,
            text=text,
            topic=topic,
            slug=slug,
            created_by=user,
        )
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=False)
        text = graphene.String(required=False)
        topic_id = graphene.Int(required=False)
        slug = graphene.String(required=False)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, title=None, text=None, topic_id=None, slug=None):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        if title is not None:
            post.title = title
        if text is not None:
            post.text = text
        if topic_id is not None:
            try:
                topic = Topic.objects.get(pk=topic_id)
                post.topic = topic
            except Topic.DoesNotExist:
                raise Exception("Invalid topic_id")
        if slug is not None:
            post.slug = slug

        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        post.delete()
        return DeletePost(ok=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)