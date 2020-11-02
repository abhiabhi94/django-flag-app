from unittest.mock import patch

from flag.signals import adjust_flagged_content
from flag.conf import settings
from tests.base import BaseFlagModelTest, Flag, FlagInstance


class FlagSignalTest(BaseFlagModelTest):
    def test_flagged_signal(self):
        user = self.user_2
        flag = self.create_flag(self.content_object_2, user)
        FlagInstance.objects.create_flag(user=user, flag=flag, reason=FlagInstance.reason_values[0], info='')
        flag.refresh_from_db()

        self.assertEqual(flag.count, 1)
        self.assertEqual(flag.state, Flag.State.FLAGGED.value)

        # instance edited won't increase the flag count
        flag_instance = FlagInstance.objects.get(user=user, flag=flag)
        self.assertIsNotNone(flag_instance)
        flag_instance.info = 'change value for test'
        flag_instance.save()
        flag.refresh_from_db()

        self.assertEqual(flag.count, 1)

    def test_unflagged_signal(self):
        user = self.user_1
        flag = self.create_flag(self.content_object_2, user)
        self.set_flag(model_obj=self.post_2, user=user)
        FlagInstance.objects.delete_flag(user=user, flag=flag)
        flag.refresh_from_db()

        self.assertEqual(flag.count, 0)
        self.assertEqual(flag.state, Flag.State.UNFLAGGED.value)

    @patch.object(settings, 'FLAG_ALLOWED', 1)
    def test_adjust_flagged_contents(self):
        post_1 = self.create_post()
        post_2 = self.create_post()
        flag_1 = Flag.objects.get_flag(post_1)
        flag_2 = Flag.objects.get_flag(post_2)

        self.assertFalse(flag_1.is_flagged)
        self.assertFalse(flag_2.is_flagged)

        self.set_flag(post_1, self.user_1)
        self.set_flag(post_1, self.user_2)

        self.set_flag(post_2, self.user_1)
        self.set_flag(post_2, self.user_2)

        flag_1.refresh_from_db()

        self.assertEqual(flag_1.count, 2)
        flag_2.refresh_from_db()

        self.assertEqual(flag_2.count, 2)

        # flagged post with wrong state will be adjusted
        flag_1.state = Flag.State.UNFLAGGED.value
        flag_1.save()
        flag_1.refresh_from_db()
        self.assertEqual(flag_1.state, Flag.State.UNFLAGGED.value)
        self.assertFalse(flag_1.is_flagged)

        # flagged post with right state => will be skipped
        flag_2.refresh_from_db()
        self.assertEqual(flag_2.state, Flag.State.FLAGGED.value)
        self.assertTrue(flag_2.is_flagged)

        adjust_flagged_content(self)
        flag_1.refresh_from_db()
        self.assertEqual(flag_1.count, 2)
        self.assertTrue(flag_1.is_flagged)
