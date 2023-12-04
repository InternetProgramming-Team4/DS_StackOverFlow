from django.db.models import Q, Count
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Major, Vote, Comment
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
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
    # major = Major.objects.get(slug=slug)  major오류로 인해 변경
    major = get_object_or_404(Major, slug=slug)
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
        context['comment_form'] = CommentForm
        user = self.request.user
        post = self.object
        content_type = ContentType.objects.get_for_model(Post)
        upvotes = Vote.objects.filter(content_type=content_type, object_id=post.id, score=Vote.UPVOTE).count()
        downvotes = Vote.objects.filter(content_type=content_type, object_id=post.id, score=Vote.DOWNVOTE).count()
        vote = upvotes - downvotes

        content_type_comment = ContentType.objects.get_for_model(Comment)
        comment_vote_counts = {}
        for comment in post.comment_set.all():
            comment_upvotes = Vote.objects.filter(content_type=content_type_comment, object_id=comment.id,
                                                  score=Vote.UPVOTE).count()
            comment_downvotes = Vote.objects.filter(content_type=content_type_comment, object_id=comment.id,
                                                    score=Vote.DOWNVOTE).count()
            comment_vote_counts[comment.pk] = comment_upvotes - comment_downvotes

        context['vote'] = vote
        context['comment_vote_counts'] = comment_vote_counts
        return context


class UpvotePostView(View):
    def post(self, request, slug, pk):
        post = get_object_or_404(Post, major__slug=slug, pk=pk)
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Post)

        # 사용자의 투표 정보 가져오기
        vote = Vote.objects.filter(content_type=content_type, object_id=post.id, voter=user).first()

        if vote and vote.score == Vote.DOWNVOTE:
            # 이미 Downvote를 한 경우에는 아무 동작도 하지 않음
            pass

        else:
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
        vote = Vote.objects.filter(content_type=content_type, object_id=post.id, voter=user).first()

        if vote and vote.score == Vote.UPVOTE:
            # 이미 Downvote를 한 경우에는 아무 동작도 하지 않음
            pass
        else:
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


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'post/register.html'
    fields = ['title', 'content', 'head_image', 'file_upload', 'major']

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'major']
    template_name = 'post/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied

    def get_success_url(self):
        return reverse('post:Qlist', kwargs={'slug': self.object.major.slug})


def new_comment(request, slug, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        return PermissionDenied


class UpvoteCommentView(View):
    def post(self, request, slug, pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Comment)

        # 사용자의 투표 정보 가져오기
        vote = Vote.objects.filter(content_type=content_type, object_id=comment.id, voter=user).first()

        if vote and vote.score == Vote.DOWNVOTE:
            # 이미 Downvote를 한 경우에는 아무 동작도 하지 않음
            pass

        else:
            if vote:
                # 이미 투표한 경우, 투표 취소
                vote.delete()
            else:
                # 투표하지 않은 경우, Upvote
                Vote.objects.create(content_type=content_type, voted_object=comment, score=Vote.UPVOTE, voter=user)

        # 리다이렉트
        return HttpResponseRedirect(reverse('post:post_detail', kwargs={'slug': slug, 'pk': str(pk)}))

class DownvoteCommentView(View):
    def post(self, request, slug, pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk)
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Comment)

        # 사용자의 투표 정보 가져오기
        vote = Vote.objects.filter(content_type=content_type, object_id=comment.id, voter=user).first()

        if vote and vote.score == Vote.UPVOTE:
            # 이미 Downvote를 한 경우에는 아무 동작도 하지 않음
            pass
        else:
            if vote:
                # 이미 투표한 경우, 투표 취소
                vote.delete()
            else:
                # 투표하지 않은 경우, Downvote
                Vote.objects.create(content_type=content_type, voted_object=comment, score=Vote.DOWNVOTE, voter=user)

        # 리다이렉트
        return HttpResponseRedirect(reverse('post:post_detail', kwargs={'slug': slug, 'pk': str(pk)}))


class PostSearchView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10  # 페이지당 아이템 수 조정 (원하는대로 변경 가능)

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-pk')
        else:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context


def post_sort(request, slug):
    major = get_object_or_404(Major, slug=slug)
    sort_option = request.GET.get('btnradio')

    if sort_option == 'popular':
        posts = Post.objects.filter(major=major).annotate(num_comments=Count('comment')).order_by('-num_comments', '-created_at')
    elif sort_option == 'latest':
        posts = Post.objects.filter(major=major).order_by('-created_at')
    elif sort_option == 'recommended':
        posts = Post.objects.filter(major=major).annotate(
            upvote_count=Count('votes', filter=Q(votes__score=1)) - Count('votes', filter=Q(votes__score=-1))
        ).order_by('-upvote_count', '-created_at')

    return render(request, 'post/post_list.html',
                  {'post_list': posts,
                   'slug': slug
                  })



