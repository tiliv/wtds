from django.views.generic import TemplateView

from wtds.wallpapers.models import Wallpaper

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'wallpapers': {
                'popular': Wallpaper.objects.popular(),
                'recent': Wallpaper.objects.recent(),
            },
        })
        return context

