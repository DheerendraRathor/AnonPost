from django.apps import AppConfig


class PostAppConfig(AppConfig):

    name = 'post'

    def ready(self):
        import post.signals

default_app_config = 'post.PostAppConfig'