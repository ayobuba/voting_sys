from django.test import TestCase
from django.utils import timezone

import datetime
from .models import Question

# Create your tests here.
class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() should return false for questions
        whose pub_date is in the future"""

        time = timezone.now() + datetime.timedelta(days=30)

        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose pub_date is older than
        one day
        :return:
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions
        whose pub_date is within the last day
        :return:
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)

def create_question(question_text,days):
    """Creates a question with the given question_text and published
    the given number of days offset to now(negative for questions published in the past , 
    positive for questions that are yet to be published"""
    time = timezone.now() +datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """if no questions exist, an appropriate message should
        be displayed"""
        
        response = self.client.get(reversed('polls:index'))
        self.assertEquals(response.status_code,200)
        
    def test_index_view_with_a_past_question(self):
        """
        Question with a pub_date in the past should be displayed on the index page.
        
        :return: 
        """
        create_question(question_text="past question",days=30)
        response = self.client.get(reversed('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
        
    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub date in the future should not be
         displayed on the the index page
        :return: 
        """
        create_question(question_text="Past question",days=30)
        create_question(question_text="Future question",days=30)
        response = self.client.get(reversed('polls:index'))
        self.assertQuerysetEqual( response.context[ 'latest_question_list' ], [ '<Question:Past question.' ] )

    def test_index_view_with_two_past_questions(self):
        """
        The question index page may display multiple
         displayedquestions.
        :return: 
        """
        create_question(question_text="Past question 1",days=30)
        create_question(question_text="Past question 2",days=-5)
        response = self.client.get(reversed('polls:index'))
        self.assertQuerysetEqual( response.context[ 'latest_question_list' ], [ '<Question:Past question 2.' ],[ '<Question:Past question 3.' ] )


class QuestionIndexDetailsTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub date in the
        future should return a 404 not found.
        :return:
        """
        future_question = create_question(question_text='Future Question',days=5)
        url = reversed('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)