# dictionary/views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import Term, Message
from .bot import DictionaryBot
bot = DictionaryBot()
class IndexView(View):
    def get(self, request):
        messages = Message.objects.all()  
        return render(request, 'dictionary/index.html', {
            'messages': messages
        })

    def post(self, request):
        user_text = request.POST.get('user_text', '').strip()
        if not user_text:
            return redirect('index')
        bot_response = bot.get_response(user_text)

        if bot_response == '__CLEAR__':
            Message.objects.all().delete() 
            return redirect('index')
        Message.objects.create(
            user_text=user_text,
            bot_response=bot_response
        )
        return redirect('index')
class AddTermView(View):
    def post(self, request):
        word = request.POST.get('word', '').lower().strip()
        definition = request.POST.get('definition', '').strip()

        if word and definition:
            Term.objects.get_or_create(
                word=word,
                defaults={'definition': definition}
            )
        return redirect('index')
    

