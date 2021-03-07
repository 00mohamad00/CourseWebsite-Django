from django.urls import reverse
from django.utils import timezone

from django.db import models
from django.utils.html import strip_tags

from account.models import Account


class Course(models.Model):
    title = models.CharField(max_length=50, blank=False , verbose_name='عنوان کلاس')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE)  # TODO: set validator
    students = models.ManyToManyField(Account, related_name='%(class)s_requests_created')

    def get_absolute_url(self):
        return reverse('course_as_teacher', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='توضیحات')
    file = models.FileField(upload_to='CourseContents', verbose_name='فایل')  # TODO: need to check
    published_date = models.DateTimeField(default=timezone.now, editable=True)

    def get_absolute_url(self):
        return reverse('course_as_teacher', kwargs={'pk': self.course.pk})

    def __str__(self):
        return self.course.title + '٬ ' + strip_tags(self.description)


class HomeWork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='درس')
    name = models.CharField(max_length=50, blank=False, verbose_name='نام')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    published_date = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(blank=False, null=False, verbose_name='آخرین مهلت ارسال')

    def get_absolute_url(self):
        return reverse('course_as_teacher', kwargs={'pk': self.course.pk})

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.FileField(upload_to='Answers', null=True, blank=True)  # TODO: need to check
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    home_work = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    submitted_date = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.student.get_full_name() + '_' + self.home_work.name
