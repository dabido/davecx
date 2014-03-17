from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from blog.models import Post, VISIBILITY_PUBLIC, VISIBILITY_UNLISTED, Tag, Category
from django.core.urlresolvers import reverse
from davecx.settings import DEBUG

@cache_page(60 * 60)
def listing(request, page=1, tag_slug=None, category_slug=None):
	visibility_mode = request.GET.get('preview', False)
	page = int(page)
	tag = None
	category = None
	show_main_teaser = True
	posts_per_page = 7

	if page > 1 or tag_slug is not None or category_slug is not None:
		show_main_teaser = False
		posts_per_page = 6

	post_list = Post.objects.all()
	if visibility_mode:
		post_list = post_list.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(visibility=VISIBILITY_UNLISTED))
	else:
		post_list = post_list.filter(visibility=VISIBILITY_PUBLIC)

	if tag_slug is not None:
		tag = get_object_or_404(Tag, slug=tag_slug)
		post_list = post_list.filter(tag__id__contains=tag.id)

	if category_slug is not None:
		category = get_object_or_404(Category, slug=category_slug)
		post_list = post_list.filter(category=category)

	if page == 2:
		post_list = post_list[1:]

	if len(post_list) == 0:
		raise Http404

	# We are using 2 paginators to correct the page number on the index page
	# One is running with 6 posts, one is running with 7.
	paginator = Paginator(post_list, posts_per_page)
	paginator_fake = Paginator(post_list, 6) # Faked paginator for correct page
	paginator_fake = paginator_fake.page(1)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger, e:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return TemplateResponse(request, 'listing.html', context=RequestContext(request, {
		'posts': posts,
		'paginator': paginator_fake,
		'tag': tag,
		'category': category,
		'show_main_teaser': show_main_teaser,
		'page': page
	}))

@cache_page(60 * 60)
def detail(request, id, slug=None):
	post = get_object_or_404(Post, Q(id=id), Q(visibility=VISIBILITY_PUBLIC) | Q(visibility=VISIBILITY_UNLISTED))
	if slug is None:
		return HttpResponseRedirect(reverse('blog.views.detail', kwargs={'id': post.id, 'slug': post.slug}))

	return TemplateResponse(request, 'detail.html', context=RequestContext(request, {
		'post': post,
		'is_dev': DEBUG
	}))

@cache_page(60 * 60)
def about(request):
	return TemplateResponse(request, 'about.html', context=RequestContext(request, {}))