from django.views.generic import TemplateView
from django.db.models import Count

from .profile.models import Profile
from .wallpapers.models import Wallpaper, Tag

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        profile = self.request.user.active_profile
        # wallpapers = Wallpaper.objects.filter_through_profile(profile)
        # tags = Tag.objects.filter_through_profile(profile)

        # FIXME: The wallpapers queryset needs to select the related tags to cut down the number of queries, but I haven't yet figured out the correct prefetch_related() or select_related() that would accomplish this.
        # wallpapers = wallpapers.prefetch_related('tagged_items')

        # most_used_tags = tags.annotate(times_used=Count('wallpaper')).order_by('-times_used')
        # recently_used_tags = tags.order_by('-wallpaper__date_created')
        # new_tags = tags.annotate(times_used=Count('wallpaper')) \
        #         .order_by('times_used', '-wallpaper__date_created')

        context.update({
            # 'tags': {
            #     'most_used': most_used_tags,
            #     'recent': recently_used_tags,
            #     'new': new_tags,
            # },
            # 'wallpapers': {
            #     'popular': wallpapers.popular(),
            #     'recent': wallpapers.recent(),
            # },
        })
        return context

