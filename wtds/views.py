from django.views.generic import TemplateView
from django.db.models import Count
from taggit.models import Tag

from .wallpapers.models import Wallpaper

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        most_used_tags = Tag.objects.annotate(times_used=Count('wallpaper')).order_by('-times_used')
        recently_used_tags = Tag.objects.order_by('-wallpaper__date_created')
        new_tags = Tag.objects.annotate(times_used=Count('wallpaper')) \
                .order_by('times_used', '-wallpaper__date_created')

        context.update({
            'tags': {
                # 'popular': ,
                'most_used': most_used_tags,
                'recent': recently_used_tags,
                'new': new_tags,
            },
            'wallpapers': {
                'popular': Wallpaper.objects.popular(),
                'recent': Wallpaper.objects.recent(),
            },
        })
        return context

