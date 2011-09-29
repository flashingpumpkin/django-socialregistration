from socialregistration.tests import SocialRegistrationTestCase

class OpenIDTest(SocialRegistrationTestCase):
    
    def test_should_redirect_to_openid_provider(self):
        response = self.client.post(self.url('openid:redirect'),
            {'openid_redirect': 'https://www.google.com/accounts/o8/id'})
        
        self.assertEqual(302, response.status_code,
            "OpenIDRedirect returned another status code: %s", response.status_code)
    
    def test_should_redirect_to_setup_view(self):
        response = self.client.get(self.url('openid:callback'))
        
        self.assertEqual(302, response.status_code,
            "OpendIDCallback returned anoth status code: %s", response.status_code)
        
