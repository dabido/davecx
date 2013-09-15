from django.conf import settings
from blog.models import VISIBILITY_PRIVATE, VISIBILITY_PUBLIC, VISIBILITY_UNLISTED, Category
import urllib

class DataProvider(object):
	def process_template_response(self, request, response):
		print "hello"
		existing_context = response.context_data
		existing_context['ABSOLUTE_URL'] = '%s' % (request.build_absolute_uri(request.get_full_path()))
		existing_context['ABSOLUTE_URL_ENCODED'] = urllib.quote(existing_context['ABSOLUTE_URL'].encode("utf-8"))
		existing_context['VISIBILITY'] = {
			'VISIBILITY_UNLISTED': VISIBILITY_UNLISTED,
			'VISIBILITY_PUBLIC': VISIBILITY_PUBLIC,
			'VISIBILITY_PRIVATE': VISIBILITY_PRIVATE
		}

		existing_context['categories'] = Category.objects.all()

		response.context_data = existing_context
		# assert False
		return response
