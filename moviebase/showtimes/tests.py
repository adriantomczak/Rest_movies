from showtimes.models import Cinema
from showtimes.serializers import CinemaSerializer
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from faker import Faker


# Create your tests here.


class CinemasTestCase(APITestCase):

    def setUp(self):

        self.faker = Faker("pl_PL")
        self.cinema = Cinema.objects.create(name=self.faker.word(), city=self.faker.city())

    def test_cinemas_list(self):
        url = reverse('cinema-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(self.cinema.name, response.data[0]['name'])
        self.assertEqual(self.cinema.city, response.data[0]['city'])

    def test_create_cinema(self):
        url = reverse('cinema-list')
        data = {
            'name': 'Multikino',
            'city': 'Warszawa',
        }
        response = self.client.post(url, data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(data['name'], response.data['name'])
        self.assertEqual(data['city'], response.data['city'])

    def test_cinema_detail(self):
        url = reverse('cinema-detail', kwargs={'pk': self.cinema.id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.cinema.name, response.data['name'])
        self.assertEqual(self.cinema.city, response.data['city'])

    def test_cinema_update(self):
        url = reverse('cinema-detail', kwargs={'pk': self.cinema.id})
        data = {
                'city': 'Warszawa',
                'name': 'Multikino',
                }
        response = self.client.put(url, data)
        self.cinema.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertEqual(data['name'], self.cinema.name)
        self.assertEqual(data['city'], self.cinema.city)

    def test_cinema_delete(self):
        url = reverse('cinema-detail', kwargs={'pk': self.cinema.id})
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Cinema.objects.filter(id=self.cinema.id).exists())
