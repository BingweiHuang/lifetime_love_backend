from django.urls import path

from main.views.literature.literature_view import LiteratureView

urlpatterns = [

    path('literature', LiteratureView.as_view(), name="literature"),
    # re_path(r".*", index, name="myspace_index"),
]