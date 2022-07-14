import datetime
from urllib import response

from django.urls.base import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently return false for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question("¿Quien es el mejor equipo de Mexico, y por que es Cruz Azul?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


def create_question(questiontext, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(questiontext=questiontext, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """si no exite ninguna pregunta, se muestra un mensaje"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        create_question("Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No hay encuestas disponibles")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def text_past_questions(self):
        question = create_question("Past Question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_questions(self):
        past_question = create_question(questiontext="Past Question", days=-30)
        future_question = create_question(questiontext="Future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        past_question1 = create_question(questiontext="Past Question 1", days=-30)
        past_question2 = create_question(questiontext="Pasr Question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question(questiontext="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        past_question = create_question(questiontext="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.questiontext)