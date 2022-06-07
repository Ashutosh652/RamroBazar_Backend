from django.shortcuts import render
from django.views import View
from ramrobazar.inventory.models import ProductOrService, Media


class HomeView(View):
	def get(self, request, *args, **kwargs):
		products_and_services = ProductOrService.objects.all()
		media = Media.objects.all()
		context = {
		'products_and_services': products_and_services,
		'media': media,
		# 'attributes': attributes,
		# 'url': url,
		}
		return render(request, 'demo/home.django-html', context)

	# def post(self, request, *args, **kwargs):
	# 	logged_in_user = request.user
	# 	posts = Post.objects.filter(
	# 		author__profile__followers__in = [logged_in_user.id]
	# 		)
	# 	form = PostForm(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		new_post = form.save(commit=False)
	# 		new_post.author = request.user
	# 		new_post.save()

	# 	context = {
	# 	'posts':posts,
	# 	'form': form
	# 	}
	# 	return render(request, 'healthpoint/home.html', context)

class DetailView(View):
	def get(self, request, slug, *args, **kwargs):
		product_or_service = ProductOrService.objects.get(slug=slug)
		context = {
			'product_or_service': product_or_service,
		}
		return render(request, 'demo/product-detail.django-html', context)