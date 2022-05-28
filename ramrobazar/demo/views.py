from django.shortcuts import render
from django.views import View
from ramrobazar.inventory.models import Product


class HomeView(View):
	def get(self, request, *args, **kwargs):
		products = Product.objects.all()
		# form = PostForm()
		context = {
		'products':products,
		}
		return render(request, 'demo/home.html', context)

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

class ProductDetailView(View):
	def get(self, request, slug, *args, **kwargs):
		product = Product.objects.get(slug=slug)
		context = {
			'product': product,
		}
		return render(request, 'demo/product-detail.html', context)