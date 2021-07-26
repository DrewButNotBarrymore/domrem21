from ads.forms import AdForm
from ads.models import Ads, Category, Images

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView


class HomeAds(ListView):
    template_name = 'ads/index.html'
    paginate_by = 8
    context_object_name = 'list_ads'

    def get_queryset(self):
        return Ads.objects.filter(is_published=True)


class MasterAds(ListView):
    template_name = 'ads/list_ads.html'
    allow_empty = False
    paginate_by = 8
    context_object_name = 'list_ads'

    def get_queryset(self):
        return Ads.objects.filter(Q(is_published=True) & Q(author__type='IM'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Объявления частных мастеров'
        return context


class CompanyAds(ListView):
    template_name = 'ads/list_ads.html'
    allow_empty = False
    paginate_by = 8
    context_object_name = 'list_ads'

    def get_queryset(self):
        return Ads.objects.filter(Q(is_published=True) & Q(author__type='CO'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Объявления компаний'
        return context


class AdsByCategory(ListView):
    model = Ads
    template_name = 'ads/list_ads.html'
    context_object_name = 'list_ads'
    allow_empty = False
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Ads.objects.filter(
            category_id=self.kwargs['category_id'], is_published=True
        ).select_related('category')


class DetailAd(DetailView):
    model = Ads
    template_name = 'ads/detail_ad.html'
    context_object_name = 'ad_item'


@login_required
def add_ad(request):
    if request.method == 'GET':
        form = AdForm()
        return render(request, 'ads/add_ad.html', {'form': form})
    elif request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            new_obj = Ads.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                category=form.cleaned_data['category'],
                phone=form.cleaned_data['phone'],
                price=form.cleaned_data['price'],
                content=form.cleaned_data['content'],
            )
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = Images(ad=new_obj)
                photo.img.save(f.name, ContentFile(data))
                photo.save()
            return redirect(new_obj)
        else:
            return render(request, 'ads/add_ad.html', {'form': form})


class Search(ListView):
    model = Ads
    template_name = 'ads/search.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master_ads'] = Ads.objects.select_related('author').filter(
            Q(title__icontains=self.request.GET.get('s'))
            | Q(content__icontains=self.request.GET.get('s')),
            is_published=1,
            author__type='IM',
        )
        context['company_ads'] = Ads.objects.select_related('author').filter(
            Q(title__icontains=self.request.GET.get('s'))
            | Q(content__icontains=self.request.GET.get('s')),
            is_published=1,
            author__type='CO',
        )
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['search_value'] = self.request.GET.get('s')
        return context


def autocomplete(request):
    query_original = request.GET.get('term')
    queryset = Category.objects.filter(
        Q(title__icontains=query_original) | Q(keys__icontains=query_original)
    )
    autocomplete_list = []
    autocomplete_list += [x.title for x in queryset]
    return JsonResponse(autocomplete_list, safe=False)


@login_required
def edit_ad(request, pk):
    current_ad = Ads.objects.get(pk=pk)
    if request.user == current_ad.author:
        if request.method == "POST":
            form = AdForm(request.POST, request.FILES, instance=current_ad)

            if form.is_valid():
                form.save()
                for f in request.FILES.getlist('photos'):
                    data = f.read()
                    photo = Images(ad=current_ad)
                    photo.img.save(f.name, ContentFile(data))
                    photo.save()
                messages.success(request, 'Ваше объявление успешно обновлено')
                return redirect('edit_ad', pk=pk)
        else:
            form = AdForm(instance=current_ad)
    else:
        return redirect('home')

    data = {'form': form, 'current_ad': current_ad}

    return render(request, 'ads/edit_ad.html', data)


@login_required
def remove_ad(request, pk):
    Ads.objects.filter(id=pk).delete()
    messages.success(request, 'Объявление успешно удалено')
    return redirect('edit_profile')


@login_required
def remove_img(request, pk):
    item = Images.objects.get(id=pk)
    if request.user == item.ad.author:
        item.delete()
        messages.success(request, 'Изображение успешно удалено')
        return redirect('edit_ad', pk=item.ad.id)
    else:
        return redirect('home')


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})
