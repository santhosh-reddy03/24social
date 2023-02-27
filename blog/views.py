from datetime import date

from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DeleteView, ListView, View

from .forms import CommentForm
from .models import Post

# Create your views here.


# def index(request):
#     all_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": all_posts})


class Index(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset()[:3]

    # def get(self, request, *args, **kwargs):
    #     all_posts = Post.objects.all().order_by("-date")[:3]
    #     return render(request, "blog/index.html", {"posts": all_posts})


class PostList(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "all_posts"
    ordering = ["-date"]


class PostDetails(View):
    # model = Post
    # template_name = "blog/post_detail.html"

    def is_saved_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            return False
        return post_id in stored_posts

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = dict()
        context["post"] = post
        context["post_tags"] = post.tags.all()
        context["comment_form"] = CommentForm
        context["comments"] = post.comments.all()
        context["is_saved_post"] = self.is_saved_post(request, post.id)
        return render(request, "blog/post_detail.html", context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("detailed_post", args=[slug]))

        context = dict()
        context["post"] = post
        context["post_tags"] = post.tags.all()
        context["comment_form"] = CommentForm
        context["comments"] = post.comments.all()
        context["is_saved_post"] = self.is_saved_post(request, post.id)
        return render(request, "blog/post_detail.html", context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm
    #     return context


# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all-posts.html", {"all_posts": all_posts})


# def detailed_post(request, slug):
#     try:
#         # post = next(post for post in all_posts if post["slug"] == slug)
#         post = get_object_or_404(Post, slug=slug)
#         return render(
#             request,
#             "blog/post_detail.html",
#             {"post": post, "post_tags": post.tags.all()},
#         )
#     except Exception as e:
#         print(e)
#         return Http404()


class ReadLaterView(View):
    def get(self, request):
        context = {"has_posts": False}
        stored_posts = request.session.get("stored_posts")
        if stored_posts:
            context["posts"] = Post.objects.filter(id__in=stored_posts)
            context["has_posts"] = True
        return render(request, "blog/stored_posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
