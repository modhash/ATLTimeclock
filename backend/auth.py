from flask import redirect, url_for, session
from flask_oauthlib.client import OAuth
import os

oauth = OAuth()
microsoft = oauth.remote_app(
    'microsoft',
    consumer_key=os.getenv('MICROSOFT_CLIENT_ID'),
    consumer_secret=os.getenv('MICROSOFT_CLIENT_SECRET'),
    request_token_params={
        'scope': 'User.Read',
        'response_type': 'code'
    },
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/authorize'
)

def setup_auth(app):
    @app.route('/mslogin')
    def mslogin():
        return microsoft.authorize(callback=url_for('authorized', _external=True))

    @app.route('/mslogout')
    def mslogout():
        session.pop('microsoft_token')
        session.pop('user_email')
        return redirect(url_for('index'))

    @app.route('/login/authorized')
    def authorized():
        response = microsoft.authorized_response()
        if response is None or response.get('access_token') is None:
            return 'Access denied: reason={} error={}'.format(
                request.args['error'], request.args['error_description']
            )

        session['microsoft_token'] = (response['access_token'], '')
        user_info = microsoft.get('me').data
        email = user_info['mail'] or user_info['userPrincipalName']
        
        # Check if user exists, if not, create a new one
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, username=email.split('@')[0])
            db.session.add(user)
            db.session.commit()

        session['user_email'] = user.email
        return redirect(url_for('profile'))

    @microsoft.tokengetter
    def get_microsoft_oauth_token():
        return session.get('microsoft_token')
