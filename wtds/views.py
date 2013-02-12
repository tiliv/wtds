from django.views.generic import TemplateView
from django.db.models import Count

from .wallpapers.models import Wallpaper, Tag

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        profile = self.request.user.profile_set.get_active()
        wallpapers = Wallpaper.objects.filter_through_profile(profile)
        tags = Tag.objects.filter_through_profile(profile)

        most_used_tags = tags.annotate(times_used=Count('wallpaper')).order_by('-times_used')
        recently_used_tags = tags.order_by('-wallpaper__date_created')
        new_tags = tags.annotate(times_used=Count('wallpaper')) \
                .order_by('times_used', '-wallpaper__date_created')

        context.update({
            'tags': {
                # 'popular': ,
                'most_used': most_used_tags,
                'recent': recently_used_tags,
                'new': new_tags,
            },
            'wallpapers': {
                'popular': wallpapers.popular(),
                'recent': wallpapers.recent(),
            },
        })
        return context

