from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtailmetadata.models import MetadataPageMixin

from wagtail.fields import RichTextField
import json

class FlightsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_template(self, request, *args, **kwargs):
        return "routes/flights_index_page.html"

class RoutePage(MetadataPageMixin, Page):
    source = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    fare_data = models.TextField(blank=True)  # we'll fill this from API
    airlines_serving_route = models.JSONField(blank=True, null=True)
    popular_routes = models.JSONField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("source"),
        FieldPanel("destination"),
        FieldPanel("fare_data"),
        FieldPanel("airlines_serving_route"),
        FieldPanel("popular_routes"),
    ]

    def get_fares(self):
        try:
            return json.loads(self.fare_data)
        except Exception:
            return []

    def get_template(self, request, *args, **kwargs):
        return "routes/route_page.html"
