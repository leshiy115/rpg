import requests
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, View)
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from .models import Announcement, Comment
from .forms import AnonsForm, CommentForm
from .filters import CommentFilter


class AnonsList(ListView):
    model = Announcement
    ordering = '-time_created'
    template_name = 'all_anons.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def comments_to_me(request):
    queryset = Comment.objects.\
            filter(anons__in=Announcement.objects.filter(author_id=request.user))

    filterset = CommentFilter(request.GET, queryset)
    context = {'all_comments': filterset.qs.order_by('-time_created'),
               'filterset': filterset}
    if request.method == "POST":
        answer = request.POST['comment'].split(' ')
        id = int(answer[0])
        accept = int(answer[1])
        Comment.objects.filter(pk=id).update(accepted=(True if accept else False))
        comment = Comment.objects.get(pk=id)
        if accept:
            html_content = render_to_string(
                'request_accepted.html',
                {
                    'user': comment.author,
                    'writer': request.user.username,
                    'anons': comment.anons,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{comment.author.username.capitalize()}',
                from_email='lutsckov.o@yandex.ru',
                to=[comment.author.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send(fail_silently=True)
            print('Отклик принят письмо с оповещением оправленно')
        else:
            Comment.objects.get(pk=id).delete()
    return render(request, 'my_list.html', context=context)



class UserDetail(LoginRequiredMixin, DetailView):
    """Для отображения профиля"""
    model = User
    template_name = "user_profile.html"
    context_object_name = 'user'


class AnonsDetail(LoginRequiredMixin, DetailView):
    """Для отображения профиля"""
    model = Announcement
    template_name = "anons_detail.html"
    context_object_name = 'anons'


class AnonsCreate(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnonsForm
    template_name = 'anons_update.html'


class AnonsUpdate(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnonsForm
    template_name = 'anons_update.html'
    success_url = reverse_lazy('all_anons')


class AnonsDelete(LoginRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'anons_delete.html'
    success_url = reverse_lazy('all_anons')

    def form_valid(self, form):
        anons = form.save(commit=False)
        anons.author = self.request.user
        return super().form_valid(form)



@login_required
def comment_create(request, pk):
    anons = Announcement.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.cleaned_data['anons'] = anons
            form.cleaned_data['author'] = request.user
            Comment.objects.create(**form.cleaned_data)
            return redirect('anons_detail', pk)
    else:
        form = CommentForm()
    context = {'anons': anons, 'form': form}
    return render(request, 'comment_create.html', context=context)



@login_required
def comment_delete(request, anons_id, pk):
    comment = get_object_or_404(Comment, pk=pk)
    context = {'comment': comment}
    if request.method == "POST":
        comment.delete()
        return redirect("anons_detail", anons_id)

    else:
        return render(request, 'comment_delete.html', context)




