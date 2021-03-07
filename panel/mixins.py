from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Course


class AccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        if course.teacher != request.user:
            raise Http404

        return super().dispatch(request)


class FormValidMixin():
    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        self.obj = form.save(commit=False)
        self.obj.course = course

        return super().form_valid(form)


class VideoValidMixin():
    def form_valid(self, form):
        video = form.cleaned_data['file']
        if 'video' not in video.content_type:
            raise Http404

        course = get_object_or_404(Course, pk=self.kwargs['pk'])

        self.obj = form.save(commit=False)
        self.obj.course = course

        return super().form_valid(form)

