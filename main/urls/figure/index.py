from django.urls import path

from main.views.figure.figure_view import FigureView

urlpatterns = [

    path('figure', FigureView.as_view(), name="figure"),
    # re_path(r".*", index, name="myspace_index"),
]