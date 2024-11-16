from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def post_login(self, request, user, *args, **kwargs):
        """
        Redirect the user to connect their Spotify account after logging in.
        """
        print("post_login")
        if not hasattr(user, 'spotifytoken'):  # Check if Spotify is already linked
            print("no token")
            return redirect('spotify_login')  # Redirect to Spotify OAuth
        return super().post_login(request, user, *args, **kwargs)
