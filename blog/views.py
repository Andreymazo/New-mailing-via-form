from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from blog.forms import ArticleForm
from blog.models import Article


# Without permissions
class ArticleListView(ListView):
    """ Вывод список статей всех: done """
    model = Article

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('blog.set_publish'):
            return queryset

        return queryset.filter(is_published=True)


class ArticleDetailView(DetailView):
    """ Вывод одной единственной статьи: done """
    model = Article

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.is_published or self.request.user.has_perm('blog.change_article'):
    #         return self.object
    #
    #     raise HttpResponseForbidden()

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_published or self.request.user.has_perm('blog.set_publish'):
            return super().get(*args, **kwargs)

        return redirect(reverse('blog:list'))


# With permissions
class ArticleCreateView(CreateView):
    model = Article
    # fields = '__all__'
    form_class = ArticleForm

    # def form_valid(self, form):
    #     article = form.save(commit=False)
    #     article.author = self.request.user
    #     #article.save()  # This is redundant, see comments.
    #     return super(ArticleCreateView, self).form_valid(form)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

class ArticleUpdateView(UpdateView):
    pass


# deprecated
# class ArticleDeleteView(DeleteView):
#     pass


# Single permission
@permission_required('blog.set_publish')
def toggle_publish(request, pk):
    current_article = get_object_or_404(Article, pk=pk)
    if current_article.is_published:
        current_article.is_published = False
    else:
        current_article.is_published = True
    current_article.save()

    return redirect(request.META.get('HTTP_REFERER'))
