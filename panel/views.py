from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, HomeWork, Answer, CourseContent
from .mixins import FormValidMixin, AccessMixin, VideoValidMixin, AccessStudentMixin, AnswerValidMixin, CourseValidMixin


@login_required
def index(request):
    return redirect('courses')


@login_required
def courses(request):
    courses_as_teacher = Course.objects.filter(teacher=request.user)

    courses_as_student = Course.objects.filter(students=request.user)

    return render(request, 'panel/courses.html', context={'courses_as_teacher': courses_as_teacher,
                                                          'courses_as_student': courses_as_student})


class CourseCreate(LoginRequiredMixin, CourseValidMixin, CreateView):
    model = Course
    fields = ['title', 'description']
    template_name = 'panel/course_create.html'


class CourseAsStudnet(AccessStudentMixin, DetailView):
    model = Course
    template_name = 'panel/course_student.html'
    context_object_name = 'course'

    def get_object(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homeworks'] = HomeWork.objects.filter(course=self.object).order_by('-published_date').all()
        context['contents'] = CourseContent.objects.filter(course=self.object).order_by('published_date').all()
        return context


class HomeworkView(AccessStudentMixin, DetailView):
    model = HomeWork
    template_name = 'panel/homework_view.html'
    context_object_name = 'homework'

    def get_object(self):
        return HomeWork.objects.get(pk=self.kwargs['pk2'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        context['homework'] = get_object_or_404(HomeWork, pk=self.kwargs['pk2'])
        submit_none_answers(context['homework'], context['course'])

        context['answer'] = Answer.objects.get(home_work=context['homework'], student=self.request.user)

        context['now'] = timezone.now()
        return context


class AnswerUpdate(AccessStudentMixin, AnswerValidMixin, UpdateView):
    model = Answer
    fields = ['answer']

    def get(self, *args, **kwargs):
        return Http404

    def get_success_url(self):
        return reverse_lazy('homework_view', kwargs={'pk': self.kwargs['pk'], 'pk2': self.kwargs['pk2']})

    def get_object(self):
        return Answer.objects.get(pk=self.kwargs['pk3'])


class CourseAsTeacher(AccessMixin, DetailView):
    model = Course
    template_name = 'panel/course_teacher.html'
    context_object_name = 'course'

    def get_object(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homeworks'] = HomeWork.objects.filter(course=self.object).order_by('-published_date').all()
        context['contents'] = CourseContent.objects.filter(course=self.object).order_by('published_date').all()
        return context


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


def submit_none_answers(homework: HomeWork, course: Course):
    answers = Answer.objects.filter(home_work=homework).order_by('-submitted_date').all()
    students_has_answer = [answer.student for answer in answers]
    students = course.students.all()
    for student in students:
        if student not in students_has_answer:
            answer = Answer()
            answer.student = student
            answer.home_work = homework
            answer.submitted_date = None
            answer.answer = None
            answer.save()


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
        submit_none_answers(context['homework'], context['course'])
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

