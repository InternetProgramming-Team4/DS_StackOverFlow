from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Major

# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-pk'


# 전공별 포스트 개수가 필요하면 사용
    # def get_context_data(self, **kwargs):
    #     context = super(PostList, self).get_context_data()
    #     context['majors'] = Major.objects.all()
    #     context['no_major_post_count'] = Post.objects.filter(major=None).count()
    #     return context


def major_page(request, slug):
    major = Major.objects.get(slug=slug)
    post_list = Post.objects.filter(major=major).order_by('-pk')

    return render (
        request,
        'post/post_list.html',
        {
            'post_list' : post_list,
            'majors' : Major.objects.all(),
            'major' : major,
        }
    )


class PostDetail(DetailView):
    model = Post
