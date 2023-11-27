from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post, Major, Vote
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        user = self.request.user
        post = self.object
        content_type = ContentType.objects.get_for_model(Post)
        vote = Vote.objects.filter(content_type=content_type, voted_object_id=post.id).count()

        context['vote'] = vote
        return context



class UpvotePostView(View):
    def post(self, request, slug, pk):
        post = get_object_or_404(Post, major__slug=slug, pk=pk)
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Post)

        # 사용자의 투표 정보 가져오기
        vote = Vote.objects.filter(content_type=content_type, voted_object_id=post.id, voter=user).first()

        if vote:
            # 이미 투표한 경우, 투표 취소
            vote.delete()
        else:
            # 투표하지 않은 경우, Upvote
            Vote.objects.create(content_type=content_type, voted_object=post, score=Vote.UPVOTE, voter=user)

        # 리다이렉트
        return HttpResponseRedirect(reverse('post:post_detail', kwargs={'slug': slug, 'pk': str(pk)}))

class DownvotePostView(View):
    def post(self, request, slug, pk):
        post = get_object_or_404(Post, major__slug=slug, pk=pk)
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Post)

        # 사용자의 투표 정보 가져오기
        vote = Vote.objects.filter(content_type=content_type, voted_object_id=post.id, voter=user).first()

        if vote:
            # 이미 투표한 경우, 투표 취소
            vote.delete()
        else:
            # 투표하지 않은 경우, Downvote
            Vote.objects.create(content_type=content_type, voted_object=post, score=Vote.DOWNVOTE, voter=user)

        # 리다이렉트
        return HttpResponseRedirect(reverse('post:post_detail', kwargs={'slug': slug, 'pk': str(pk)}))


def nomajorlist(request):
    return render(
        request,
        'post/Qlist.html'
    )

