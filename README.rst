<h1 id="django-social-registration">Django Social Registration</h1>
<p>Django Social Registration enables developers to add alternative registration methods based on third party sites.</p>
<p>Supported methods currently are:</p>
<ul>
<li>OpenID</li>
<li>OAuth</li>
<li>Facebook Connect</li>
</ul>
<h2 id="requirements">Requirements</h2>
<ul>
<li><a href="http://pypi.python.org/pypi/django/">Django</a></li>
<li><a href="http://pypi.python.org/pypi/oauth2/">oauth2</a></li>
<li><a href="http://pypi.python.org/pypi/python-openid">python-openid</a></li>
<li><a href="https://github.com/facebook/python-sdk">python-sdk</a></li>
</ul>
<h2 id="installation">Installation</h2>
<pre><code>    pip install django-socialregistration
    pip install -e git+https://github.com/facebook/python-sdk.git#egg=FacebookSDK
</code></pre>
<h2 id="configuration">Configuration</h2>
<ol style="list-style-type: decimal">
<li>Add <code>socialregistration</code> to your <code>INSTALLED_APPS</code></li>
<li>Add <code>django.core.context_processors.request</code> to the <a href="http://docs.djangoproject.com/en/1.3/ref/settings/#template-context-processors">TEMPLATE_CONTEXT_PROCESSORS</a></li>
<li><p>Include <code>socialregistration.urls</code> in your top level urls:</p>
<pre><code>urlpatterns = patterns('', 
    # ...
    url(r'^social/', include('socialregistration.urls')))
</code></pre></li>
<li><p>Make sure you are using a <a href="http://docs.djangoproject.com/en/1.3/ref/templates/api/#subclassing-context-requestcontext">RequestContext</a> wherever you are planning to display the login buttons</p>
<pre><code>from django.template import RequestContext

def login(request):
    # ...
    return render_to_response('login.html',
        {}, context_instance = RequestContext(request))
</code></pre></li>
<li><p>Once you're done, and configured, etc, don't forget to <code>python manage.py syncdb</code> your project.</p></li>
</ol>
<h2 id="facebook-connect">Facebook Connect</h2>
<h4 id="configuration-1">Configuration</h4>
<ol style="list-style-type: decimal">
<li><p>Add the Facebook API keys to the your settings, variable names are</p>
<pre><code>FACEBOOK_APP_ID = ''
FACEBOOK_API_KEY = ''
FACEBOOK_SECRET_KEY = ''
</code></pre></li>
<li>Add <code>socialregistration.auth.FacebookAuth</code> to <a href="http://docs.djangoproject.com/en/1.3/ref/settings/#authentication-backends">AUTHENTICATION_BACKENDS</a></li>
<li>Add <code>socialregistration.middleware.FacebookMiddleware</code> to <a href="http://docs.djangoproject.com/en/1.3/ref/settings/#middleware-classes">MIDDLEWARE_CLASSES</a></li>
<li><p>(Optional) Add <code>FACEBOOK_REQUEST_PERMISSIONS</code> to your settings. This is a comma seperated list of the permissions you need. e.g:</p>
<pre><code>FACEBOOK_REQUEST_PERMISSIONS = 'email,user_about_me'
</code></pre></li>
</ol>
<h4 id="usage">Usage</h4>
<ul>
<li><p>Add tags to your template file</p>
<pre><code>{% load facebook_tags %}
{% facebook_button %}
{% facebook_js %}
</code></pre></li>
</ul>
<p>You can also specify your own custom button image by appending it to the <code>facebook_button</code> template tag:</p>
<pre><code>    {% facebook_button 'http://example.com/other_facebook_button.png' %}
</code></pre>
<p>You want to keep the <code>{% facebook_js %}</code> as far down in your HTML structure as possible to not impact the load time of the page.</p>
<p>Also make sure you followed the steps to include a <code>RequestContext</code> in your template that is using these tags.</p>
<h2 id="twitter">Twitter</h2>
<h4 id="configuration-2">Configuration</h4>
<ol style="list-style-type: decimal">
<li><p>Add the Twitter API keys and endpoints to your settings, variable names are</p>
<pre><code>TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET_KEY = ''
TWITTER_REQUEST_TOKEN_URL = ''
TWITTER_ACCESS_TOKEN_URL = ''
TWITTER_AUTHORIZATION_URL = ''
</code></pre></li>
<li>Add <code>socialregistration.auth.TwitterAuth</code> to <code>AUTHENTICATION_BACKENDS</code></li>
<li><p>Add the right callback URL to your Twitter account</p></li>
</ol>
<h4 id="usage-1">Usage</h4>
<ul>
<li><p>Add tags to your template file</p>
<pre><code>{% load twitter_tags %}
{% twitter_button %}
</code></pre></li>
</ul>
<p>Same note here. Make sure you're serving the page with a <code>RequestContext</code></p>
<p>You can also specify your own custom button image by appending it to the <code>twitter_button</code> template tag:</p>
<pre><code>    {% twitter_button 'http://example.com/other_twitter_button.png' %}
</code></pre>
<h2 id="linkedin">LinkedIn</h2>
<h4 id="configuration-3">Configuration</h4>
<ol style="list-style-type: decimal">
<li><p>Add the LinkedIn API keys and endpoints to your settings, variable names are</p>
<pre><code>    LINKEDIN_CONSUMER_KEY = ''
LINKEDIN_CONSUMER_SECRET_KEY = ''
LINKEDIN_REQUEST_TOKEN_URL = ''
LINKEDIN_ACCESS_TOKEN_URL = ''
LINKEDIN_AUTHORIZATION_URL = ''
</code></pre></li>
<li>Add <code>socialregistration.auth.LinkedInAuth</code> to <code>AUTHENTICATION_BACKENDS</code></li>
<li><p>Add the right callback URL to your LinkedIn account</p></li>
</ol>
<h4 id="usage-2">Usage</h4>
<ul>
<li><p>Add tags to your template file</p>
<pre><code>{% load linkedin_tags %}
{% linkedin_button %}
</code></pre></li>
</ul>
<p>Same note here. Make sure you're serving the page with a <code>RequestContext</code></p>
<p>You can also specify your own custom button image by appending it to the <code>linkedin_button</code> template tag:</p>
<pre><code>    {% linkedin_button 'http://example.com/other_linkedin_button.png' %}
</code></pre>
<h2 id="oauth">OAuth</h2>
<p>Check out how the Twitter authentication works. Basically it's just plugging together some urls and creating an auth backend, a model and a view.</p>
<h2 id="openid">OpenID</h2>
<h4 id="configuration-4">Configuration</h4>
<ul>
<li>Add <code>socialregistration.auth.OpenIDAuth</code> to <code>AUTHENTICATION_BACKENDS</code></li>
</ul>
<h4 id="usage-3">Usage</h4>
<ul>
<li><p>Add tags to your template file</p>
<pre><code>{% load openid_tags %}
{% openid_form %}
</code></pre></li>
</ul>
<h2 id="logging-users-out">Logging users out</h2>
<p>You can use the standard <code>{% url auth_logout %}</code>. Alternatively there is also <code>{% url social_logout %}</code> which is basically a wrapper around <code>auth_logout</code>.</p>
<p><em>This will log users only out of your site</em>.</p>
<p>To make sure they're logged out of other sites too, use something like this:</p>
<pre><code>    &lt;a href=&quot;#&quot; onclick:&quot;javascript:FB.logout(function(resp){ document.location = '{% url social_logout %}'; })&quot;&gt;Logout&lt;/a&gt;
</code></pre>
<p>Or redirect them to the provider they logged in from.</p>
<h2 id="additional-settings">Additional Settings</h2>
<pre><code>    SOCIALREGISTRATION_USE_HTTP = False
    SOCIALREGISTRATION_GENERATE_USERNAME = False
</code></pre>
<p>Set either <code>True</code> if you want to enable HTTPS or have the users skip the username form.</p>
<h2 id="signals">Signals</h2>
<p>The app provides two signals that fire when users connect their accounts and log in:</p>
<pre><code>    socialregistration.signals.connect
    socialregistration.signals.login
</code></pre>
<p>The signal handlers needs to accept three arguments, and can listen on specific profiles:</p>
<pre><code>    from socialregistration import signals
    from socialregistration import models

    def connect_facebook(user, profile, client, **kwargs):
        # Do fancy stuff like fetching more user info with the client
        pass

    def login_facebook(user, profile, client, **kwargs):
        # Do fancy stuff like finding logged in friends
        pass

    signals.connect.connect(connect_facebook, sender = models.FacebookProfile)
    signals.login.connect(login_facebook, sender = models.FacebookProfile)
</code></pre>
<p>This works too with OpenID and OAuth profiles.</p>
<h1 id="release-notes">Release Notes</h1>
<h3 id="v0.4.6"><em>v0.4.6</em></h3>
<ul>
<li>Added LinkedIn support</li>
<li>Bugfixes and OAuth2 beginnings for Facebook</li>
</ul>
