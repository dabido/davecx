from django.conf import settings
from blog.models import VISIBILITY_PRIVATE, VISIBILITY_PUBLIC, VISIBILITY_UNLISTED, Category
import urllib

def provide_data(request):
	context = {}
	context['ABSOLUTE_URL'] = '%s' % (request.build_absolute_uri(request.get_full_path()))
	context['ABSOLUTE_URL_ENCODED'] = urllib.quote(context['ABSOLUTE_URL'].encode("utf-8"))
	context['VISIBILITY'] = {
		'VISIBILITY_UNLISTED': VISIBILITY_UNLISTED,
		'VISIBILITY_PUBLIC': VISIBILITY_PUBLIC,
		'VISIBILITY_PRIVATE': VISIBILITY_PRIVATE
	}
	context['ASSET_VERSION'] = settings.ASSET_VERSION

	context['categories'] = Category.objects.all()

	return context