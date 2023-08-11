from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .forms import  NoticeRequestForm
from .models import  *
from django.db.models import Q

# Vacate Notice views
class NoticeView(View):
    def get(self, request):
        form = NoticeRequestForm()
        notices=Notice.objects.filter(Q(read=False) & (Q(notify_specific_user=request.user) | Q(notify_group_of_users=request.user.user_type)))
        return render(request, 'notices/notice_home.html', {'form': form,'notices':notices,'page_title':'New Notification'})

    def post(self, request):
        form = NoticeRequestForm(request.POST)
        notices=Notice.objects.filter(Q(notify_specific_user=request.user) | Q(user=request.user))
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user=request.user
            notice.save()
            messages.success(request, "Notice sent!")
            return redirect('notice_add')
        return render(request, 'notices/notice_home.html', {'form': form,'notices':notices,'page_title':'New Notification'})

class NoticeDetail(View):
    def get(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        notice.read=True
        notice.save()
        return render(request, 'notices/notice_detail.html', {'notice':notice})

    def post(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        reply =request.POST.get('reply')
        NoticeFeedback.objects.create(notice=notice,user=request.user,reply=reply)
        messages.success(request, "Reply sent!")
        return redirect('notice-detail', pk=pk)
