from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from user.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.habit = Habit.objects.create(
            owner=self.user,
            place="качалка",
            time="2024-08-24T08:00:00",
            action="обед",
            is_pleasant=False,
            reward="пойти поучить drf",
            periodicity=1,
            time_to_complete=120,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habit:habit-list")
        data = {
            "place": "дом",
            "time": "2024-07-24T20:40:00",
            "action": "учить django",
            "is_pleasant": False,
            "reward": "выпить сок",
            "periodicity": 1,
            "time_to_complete": 120,
            "is_public": True,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        url = reverse("habit:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        data = {
            "reward": "выпить сок",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "выпить сок")

    def test_public_habit_list(self):
        url = reverse("habit:public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)