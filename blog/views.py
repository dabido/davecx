from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from blog.models import Post, VISIBILITY_PUBLIC, VISIBILITY_UNLISTED, Tag, Category

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

	paginator = Paginator(post_list, posts_per_page)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger, e:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return TemplateResponse(request, 'listing.html', {
		'posts': posts,
		'tag': tag,
		'category': category,
		'show_main_teaser': show_main_teaser,
		'page': page
	})

def detail(request, id, slug):
	post = get_object_or_404(Post, Q(id=id), Q(visibility=VISIBILITY_PUBLIC) | Q(visibility=VISIBILITY_UNLISTED))

	return TemplateResponse(request, 'detail.html', {
		'post': post
	})

def about(request):
	return TemplateResponse(request, 'about.html', {})