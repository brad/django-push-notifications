import mock
from django.test import TestCase
from push_notifications.models import GCMDevice, APNSDevice


class ModelTestCase(TestCase):
	def test_can_save_gcm_device(self):
		device = GCMDevice.objects.create(
			registration_id="a valid registration id",
		)
		assert device.id is not None

	def test_can_create_save_device(self):
		device = APNSDevice.objects.create(
			registration_id="a valid registration id",
		)
		assert device.id is not None

	def test_gcm_send_message(self):
		device = GCMDevice.objects.create(
			registration_id="abc",
		)
		with mock.patch("push_notifications.gcm._gcm_send") as p:
			device.send_message("Hello world")
			p.assert_called_once_with(
				'registration_id=abc&data.message=Hello+world',
				'application/x-www-form-urlencoded;charset=UTF-8')

	def test_gcm_send_message_extra(self):
		device = GCMDevice.objects.create(
			registration_id="abc",
		)
		with mock.patch("push_notifications.gcm._gcm_send") as p:
			device.send_message("Hello world", extra={"foo": "bar"})
			p.assert_called_once_with(
				'registration_id=abc&data.foo=bar&data.message=Hello+world',
				'application/x-www-form-urlencoded;charset=UTF-8')

	def test_apns_send_message(self):
		device = APNSDevice.objects.create(
			registration_id="abc",
		)
		socket = mock.MagicMock()
		with mock.patch("push_notifications.apns._apns_pack_message") as p:
			device.send_message("Hello world", socket=socket)
			p.assert_called_once_with('abc', '{"aps":{"alert":"Hello world"}}')

	def test_apns_send_message_extra(self):
		device = APNSDevice.objects.create(
			registration_id="abc",
		)
		socket = mock.MagicMock()
		with mock.patch("push_notifications.apns._apns_pack_message") as p:
			device.send_message("Hello world", extra={"foo": "bar"}, socket=socket)
			p.assert_called_once_with('abc', '{"aps":{"alert":"Hello world"},"foo":"bar"}')
