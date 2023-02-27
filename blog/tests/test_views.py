from datetime import date

from django.core.files import File
from django.test import TestCase

from blog import views
from blog.models import Author, Comment, Post, Tags


class TestIndexView(TestCase):
    def setUp(self) -> None:
        author = Author.objects.create(first_name="Tony", last_name="Stark", email="tony@starktech.com")
        tag = [Tags.objects.create(caption=i) for i in ["new", "recent"]]
        for i, v in enumerate(["coding.png", "mountains.jpg", "woods.jpg"]):
            with open(f"blog/tests/images_test/{v}", "rb") as fp:
                post = Post(
                    image=File(fp, name=v),
                    author=author,
                    date=date.today(),
                    title=f"hello world {i}",
                    excerpt="how i begin my coding career",
                    content=f"test {i}",
                )
                post.save()
                post.tags.add(*tag)
                post.save()

    def test_index_response(self):
        response = self.client.get("/")
        self.assertEqual(len(response.context["posts"]), 3)
        self.assertIs(response.resolver_match.func.view_class, views.Index)
        self.assertIs(response.resolver_match.view_name, "index")
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        Post.objects.all().delete()
        return super().tearDown()
