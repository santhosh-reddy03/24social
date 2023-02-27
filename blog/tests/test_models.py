from datetime import date

from django.core.files import File
from django.test import TestCase

from blog.models import Author, Comment, Post, Tags

# Create your tests here.


class AuthorTestCase(TestCase):
    def setUp(self) -> None:
        Author.objects.create(first_name="Tony", last_name="Stark", email="")

    def test_author_created(self):
        author = Author.objects.get(first_name="Tony")
        self.assertEqual(author.last_name, "Stark")


class PostCommentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        author = Author.objects.create(first_name="Tony", last_name="Stark", email="")
        tag = [Tags.objects.create(caption=i) for i in ["new", "recent"]]
        for i, v in enumerate(["coding.png", "mountains.jpg", "woods.jpg"]):
            with open(f"blog/tests/images_test/{v}", "rb") as fp:
                post = Post(
                    image=File(fp, name=f"{v}"),
                    author=author,
                    date=date.today(),
                    title=f"hello world {i}",
                    excerpt="how i begin my coding career",
                    content=f"test test test {i}",
                )
                post.save()
                post.tags.add(*tag)
                comment = Comment(
                    user_name="santhosh",
                    user_email="santhosh@test.com",
                    text="this is awesome post",
                    post=post,
                )
                comment.save()
        return super().setUpTestData()

    # def setUp(self) -> None:

    def test_post(self):
        self.assertEqual(len(Post.objects.all()), 3)

    def test_comment(self):
        self.assertEqual(len(Comment.objects.all()), 3)

    def tearDown(self) -> None:
        Post.objects.all().delete()
        return super().tearDown()
