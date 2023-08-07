from django.views.generic import RedirectView


class ToAdminRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/admin'

