from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.models import UserProfile, GameSessionData

# Import modules
from main.card import CardManager
from main.game_session import GameSession

class MainView(View):

    card = CardManager()

    def get(self, request):
        if request.user.is_authenticated:
            card_user_name = self.card.getUserFullName(request)
            card_account_number = self.card.getAccountNumber(request)
            card_remaining_conins = self.card.getRemainingCoins(request)

            return render(request, 'pages/index.html',
                {
                    'card_name': card_user_name,
                    'card_account_number': card_account_number,
                    'card_remaining_conins': card_remaining_conins,
                })
        else:
            return render(request, 'pages/login.html')


class DillerView(View):

    card = CardManager()

    def get(self, request):
        if request.user.is_authenticated:
            card_user_name = self.card.getUserFullName(request)
            card_account_number = self.card.getAccountNumber(request)
            card_remaining_conins = self.card.getRemainingCoins(request)

            return render(request, 'pages/diller.html',
                {
                    'card_name': card_user_name,
                    'card_account_number': card_account_number,
                    'card_remaining_conins': card_remaining_conins,
                })
        else:
            return render(request, 'pages/login.html')


class DillerSessionView(View):
    sess = GameSession()

    def get(self, request):
        if request.user.is_authenticated:
            session_info = self.sess.createSession(request)
            return render(request, 'pages/session.html', {
                'session_id': session_info[0],
                'session_pin': session_info[1]
            })
        else:
            return render(request, 'pages/login.html')

    def post(self, request):
        req_type = request.POST['post_type']
        session_id = request.POST['session_id']
        if req_type == "end_session":
            self.sess.revokeSession(session_id)
            return HttpResponseRedirect('/')


class PairingView(View):
    sess = GameSession()


    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'pages/pairing.html')
        else:
            return render(request, 'pages/login.html')

    def post(self, request):
        passcode = request.POST['passcode']
        for db in GameSessionData.objects.all():
            if passcode == db.session_passwd:
                if db.isRevoked:
                    return render(request, 'pages/pairing.html', {'error': "無効なセッションです。"})

                self.sess.addMember(request, passcode)
                return HttpResponseRedirect('/')
        return render(request, 'pages/pairing.html', {'error': "パスが違います。"})
