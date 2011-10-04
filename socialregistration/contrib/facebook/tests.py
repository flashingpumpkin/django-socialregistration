from socialregistration.tests import TemplateTagTest


class TestTemplateTag(TemplateTagTest):
    def get_tag(self):
        return 'facebook', 'facebook_button'
