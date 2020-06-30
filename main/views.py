from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from main.forms import MessagesForm, MessagesDetailForm
from main.models import Messages


class MainView(View):

    def get(self, request):
        return render(request, '__base__.html')


class MessageListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'msg_list.html', {'messages': Messages.objects.filter(send_to=request.user)})


class MessageView(LoginRequiredMixin, View):
    def get(self, request, pk):
        msg = Messages.objects.get(pk=pk)
        msg.is_read = True
        msg.save()
        form = MessagesDetailForm(instance=msg)
        return render(request, 'generic_form.html', {'form': form, 'title': msg.title})


class SendMessageView(LoginRequiredMixin, View):
    def get(self, request):
        form = MessagesForm()
        return render(request, 'generic_form.html', {'form': form, 'button': 'Wyślij', 'title': 'Wyślij wiadomość'})

    def post(self, request):
        form = MessagesForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.send_by = request.user
            msg.save()
            return redirect(reverse_lazy('messages'))
        return render(request, 'generic_form.html', {'form': form, 'button': 'Wyślij', 'title': 'Wyślij wiadomość'})
