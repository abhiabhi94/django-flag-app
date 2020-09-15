from django.core.exceptions import ValidationError

from tests.base import BaseFlagModelTest, Flag, FlagInstance


class FlagModelTest(BaseFlagModelTest):
    def test_can_create_flag(self):
        self.assertIsNotNone(Flag.objects.create(content_object=self.post_2))

    def test_increase_count(self):
        self.flag.increase_count()
        self.flag.refresh_from_db()

        self.assertEqual(self.flag.count, 1)

    def test_decrease_count(self):
        self.flag.increase_count()
        self.flag.decrease_count()
        self.flag.refresh_from_db()

        self.assertEqual(self.flag.count, 0)

    def test_get_clean_state(self):
        flag = self.flag
        state = flag.get_clean_state(Flag.State.FLAGGED.value)
        self.assertEqual(state, Flag.State.FLAGGED.value)

        # int not in existing states
        self.assertRaises(ValidationError, flag.get_clean_state, 100)

        # not int
        self.assertRaises(ValidationError, flag.get_clean_state, 'Not int')

        # None
        self.assertRaises(ValidationError, flag.get_clean_state, None)

    def test_toggle_state(self):
        post = self.content_object_2
        flag = self.create_flag(post)
        self.assertIsNone(flag.moderator)
        self.assertEqual(flag.state, flag.State.UNFLAGGED.value)

        # toggle states occurs between rejected and resolved only
        self.assertRaises(ValidationError, flag.toggle_state, flag.State.FLAGGED.value, self.moderator)

        flag.toggle_state(flag.State.REJECTED.value, self.moderator)
        self.assertEqual(flag.state, flag.State.REJECTED.value)
        self.assertEqual(flag.moderator, self.moderator)

        # passing RESOLVED state value for the first time
        flag.toggle_state(flag.State.RESOLVED.value, self.moderator)
        self.assertEqual(flag.state, flag.State.RESOLVED.value)

        # passing RESOLVED state value for the second time
        flag.toggle_state(flag.State.RESOLVED.value, self.moderator)
        # state reset to FLAGGED
        self.assertEqual(flag.state, flag.State.FLAGGED.value)

    def test_toggle_flagged_state(self):
        self.flag.increase_count()
        self.flag.toggle_flagged_state()

        self.assertEqual(self.flag.state, Flag.State.FLAGGED.value)

        with self.settings(FLAGS_ALLOWED=1):
            self.flag.count = 0
            self.flag.save()
            self.flag.increase_count()
            self.flag.toggle_flagged_state()

            self.assertEqual(self.flag.state, Flag.State.UNFLAGGED.value)
            # flag once more to toggle the state
            self.flag.increase_count()
            self.flag.toggle_flagged_state()

            self.assertEqual(self.flag.state, Flag.State.FLAGGED.value)


class FlagManagerTest(BaseFlagModelTest):
    def setUp(self):
        super().setUp()
        self.flag = Flag.objects.create(content_object=self.content_object_2, creator=self.post_2.user)

    def test_get_flag(self):
        self.assertEqual(Flag.objects.get_flag(self.post_2), self.flag)


class FlagInstanceModelTest(BaseFlagModelTest):
    def test_create_flag_instance(self):
        self.assertIsNotNone(
            FlagInstance.objects.create(
                flag=self.flag,
                reason=FlagInstance.reason_values[0],
                user=self.user_1
            )
        )


class TestFlagInstanceManager(BaseFlagModelTest):

    def test_has_flagged(self):
        user = self.user_2
        post = self.post_2
        self.assertEqual(FlagInstance.objects.has_flagged(user, post), False)

        self.set_flag(self.post_2, user=user)

        self.assertEqual(FlagInstance.objects.has_flagged(user, post), True)

    def test_clean_when_last_reason_is_used(self):
        flag = self.flag

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create(
                flag=flag,
                reason=FlagInstance.reason_values[-1]
            )
        self.assertEqual(
            error.exception.message_dict['info'],
            ['Please provide some information why you choose to report the content'])

    def test_clean_reason_for_invalid_values(self):
        flag = self.flag
        user = self.user_1
        reason = -1
        info = None

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

        reason = 'r'
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

        reason = None
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

    def test_create_flag_for_flagging_twice(self):
        user = self.user_1
        flag = self.flag
        reason = FlagInstance.reason_values[0]
        info = None

        FlagInstance.objects.create_flag(user, flag, reason, info)
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user, flag, reason, info)

        self.assertEqual(error.exception.messages, [f'This content has already been flagged by the user ({user})'])

    def test_delete_flag_without_flagging(self):
        user = self.user_1
        flag = self.flag

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.delete_flag(user, flag)

        self.assertEqual(error.exception.messages, [f'This content has not been flagged by the user ({user})'])
