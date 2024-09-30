from silica import Component
from silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest


class Properties(Component):
    foo = "bar"

    def inline_template(self):
        return """
            <div>{{ foo }}</div>
        """


class PropertiesTestCase(SilicaTestCase):
    def test_can_set_properties(self):
        (
            SilicaTest(component=Properties)
            .assertSet("foo", "bar")
            .assertSee("bar")
            .set("foo", "boo")
            .assertSet("foo", "boo")
            .assertSee("boo")
        )
