import re
import markdown
from pure_pagination.mixins import PaginationMixin
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
# Create your views here.


# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    paginate_by = 10


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         # 记得在顶部引入 TocExtension 和 slugify
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)

#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''

#     return render(request, 'blog/detail.html', context={'post': post})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    # def get_object(self, queryset=None):
    #     # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         # 记得在顶部引入 TocExtension 和 slugify
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)

    #     m = re.search(
    #         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''

    #     return post


# def archive(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     )
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

# def category(request, pk):
#     # 记得在开始部分导入 Category 类
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# def tag(request, pk):
#     # 记得在开始部分导入 Tag 类
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class TagView(IndexView):

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, message.ERROR,
                             error_msg, extra_tags="danger")
        return redirect('blog:index')

    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list':post_list})