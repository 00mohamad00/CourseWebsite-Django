from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, HomeWork, Answer, CourseContent
from .mixins import FormValidMixin, AccessMixin, VideoValidMixin


@login_required
def index(request):
    return redirect('courses')
    title = 'hassani good boy'
    return render(request, 'panel/index.html', context={'user': request.user, 'title': title})


@login_required
def courses(request):
    courses_as_teacher = Course.objects.filter(teacher=request.user)

    courses_as_student = Course.objects.filter(students=request.user)

    return render(request, 'panel/courses.html', context={'courses_as_teacher': courses_as_teacher,
                                                          'courses_as_student': courses_as_student})


class CourseAsTeacher(AccessMixin, DetailView):
    model = Course
    template_name = 'panel/course_teacher.html'
    context_object_name = 'course'

    def get_object(self):
        return Course.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homeworks'] = HomeWork.objects.filter(course=self.object).order_by('-published_date').all()
        context['contents'] = CourseContent.objects.filter(course=self.object).order_by('published_date').all()
        return context


@login_required
def course_as_student(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user not in course.students.all():
        return redirect('index')

    context = {
        'title': course.title,
        'description': course.description,
    }

    return render(request, 'panel/course_student.html', context=context)


class HomeworkCreate(AccessMixin, FormValidMixin, CreateView):
    model = HomeWork
    fields = ['name', 'description', 'deadline_date']
    template_name = 'panel/create_change_homework.html'


class HomeworkUpdate(AccessMixin, FormValidMixin, UpdateView):
    model = HomeWork
    fields = ['name', 'description', 'deadline_date']
    template_name = 'panel/create_change_homework.html'

    def get_object(self):
        return HomeWork.objects.get(pk=self.kwargs['pk2'])


class HomeworkDelete(AccessMixin, DeleteView):
    model = HomeWork

    def get(self, *args, **kwargs):
        return Http404

    def get_success_url(self):
        course_pk = self.kwargs['pk']
        return reverse_lazy('course_as_teacher', kwargs={'pk': course_pk})

    def get_object(self):
        return HomeWork.objects.get(pk=self.kwargs['pk2'])


class HomeworkAnswers(AccessMixin, ListView):
    model = HomeWork
    template_name = 'panel/homework_answers.html'
    context_object_name = 'answers'

    def get_queryset(self):
        self.homework = get_object_or_404(HomeWork, pk=self.kwargs['pk2'])
        return Answer.objects.filter(home_work=self.homework).order_by('-submitted_date').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['homework'] = get_object_or_404(HomeWork, pk=self.kwargs['pk2'])
        return context


class AnswerScoreUpdate(AccessMixin, UpdateView):
    model = Answer
    fields = ['score']

    def get(self, *args, **kwargs):
        return Http404

    def get_success_url(self):
        return reverse_lazy('homework_answers', kwargs={'pk': self.kwargs['pk'], 'pk2': self.kwargs['pk2']})

    def get_object(self):
        return Answer.objects.get(pk=self.kwargs['pk3'])


class ContentCreate(AccessMixin, VideoValidMixin, CreateView):
    model = CourseContent
    fields = ['description', 'file']
    template_name = 'panel/create_change_content.html'


class ContentDelete(AccessMixin, DeleteView):
    model = HomeWork

    def get(self, *args, **kwargs):
        return Http404

    def get_success_url(self):
        course_pk = self.kwargs['pk']
        return reverse_lazy('course_as_teacher', kwargs={'pk': course_pk})

    def get_object(self):
        return CourseContent.objects.get(pk=self.kwargs['pk2'])

