# from django.test import RequestFactory, TestCase
# from django.urls import reverse

# from .views import chat

# class ChatViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_chat_view(self):
#         url = reverse('chat')  # Assuming 'chat' is the name of the URL pattern for the 'chat' view
#         request = self.factory.get(url)
#         response = chat(request)

#         self.assertEqual(response.status_code, 200)  # Check if the response status code is 200
#         self.assertTemplateUsed(response, 'chat.html')  # Check if the correct template is used
