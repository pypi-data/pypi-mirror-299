import inspect
from unittest import TestCase

from django.contrib.auth import get_user_model

from django_functest import AdminLoginMixin, FuncBaseMixin, FuncSeleniumMixin, FuncWebTestMixin, ShortcutLoginMixin

from .base import ChromeBase, FirefoxBase, WebTestBase

LOGGED_OUT_URL = "/admin/login/?next=/admin/"


class TestShortcutLoginBase(ShortcutLoginMixin):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "password")

    def test_login_succeeds(self):
        self.shortcut_login(username=self.user.username, password="password")
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_raises_exception_with_wrong_password(self):
        self.assertRaises(
            ValueError,
            lambda: self.shortcut_login(username=self.user.username, password="foo"),
        )

    def test_logout_succeeds(self):
        self.shortcut_login(username=self.user.username, password="password")
        self.shortcut_logout()
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)


class TestShortcutLoginWebTest(TestShortcutLoginBase, WebTestBase):
    pass


class TestShortcutLoginFirefox(TestShortcutLoginBase, FirefoxBase):
    pass


class TestShortcutLoginChrome(TestShortcutLoginBase, ChromeBase):
    pass


class TestAdminLoginBase(AdminLoginMixin):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "password")

    def test_login_succeeds(self):
        self.do_login(username="admin", password="password", shortcut=False)
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_shortcut_succeeds(self):
        self.do_login(username="admin", password="password", shortcut=True)
        self.get_url("admin:index")
        self.assertUrlsEqual("/admin/")

    def test_login_raises_exception_with_wrong_password(self):
        self.assertRaises(ValueError, lambda: self.do_login(username="admin", password="password_2"))

    def test_logout_succeeds(self):
        self.shortcut_login(username="admin", password="password")
        self.do_logout(shortcut=True)
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)

    def test_logout_shortcut_succeeds(self):
        self.shortcut_login(username="admin", password="password")
        self.do_logout(shortcut=False)
        self.get_url("admin:index")
        self.assertUrlsEqual(LOGGED_OUT_URL)

    def test_shortcut_session_data(self):
        self.do_login(username="admin", password="password", shortcut=False)
        logged_in_session_data = self.get_session_data()
        self.get_url("admin:logout")
        logged_out_session_data = self.get_session_data()
        assert not logged_out_session_data

        # The shortcut method should produce the same session data
        # as the real method.
        self.shortcut_login(username="admin", password="password")
        logged_in_session_data_shortcut = self.get_session_data()
        self.shortcut_logout()
        logged_out_session_data_shortcut = self.get_session_data()
        self.assertEqual(logged_in_session_data, logged_in_session_data_shortcut)
        self.assertEqual(logged_out_session_data, logged_out_session_data_shortcut)


class TestAdminLoginWebTest(TestAdminLoginBase, WebTestBase):
    pass


class TestAdminLoginFirefox(TestAdminLoginBase, FirefoxBase):
    pass


class TestAdminLoginChrome(TestAdminLoginBase, ChromeBase):
    pass


class TestDocStrings(TestCase):
    def test_doc_strings(self):
        bad_docstrings = []
        for cls in [FuncSeleniumMixin, FuncWebTestMixin]:
            for name, member in inspect.getmembers(cls):
                if name.startswith("__"):
                    continue
                member_doc = getattr(member, "__doc__", None)

                base_member = getattr(FuncBaseMixin, name, None)
                if base_member is not None:
                    base_doc = getattr(base_member, "__doc__", None)
                    if base_doc is not None and member_doc != base_doc:
                        bad_docstrings.append((cls, name))

        if bad_docstrings:
            self.fail(
                "The following methods have incorrect or missing docstrings "
                "compared to FuncBaseMixin: \n" + "\n".join(f"{cls.__name__}.{name}" for cls, name in bad_docstrings)
            )
