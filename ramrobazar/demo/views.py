from django.shortcuts import render
from django.views import View
from ramrobazar.inventory.models import Item, Media


class HomeView(View):
	def get(self, request, *args, **kwargs):
		products_and_services = Item.objects.all()
		media = Media.objects.all()
		context = {
		'products_and_services': products_and_services,
		'media': media,
		# 'attributes': attributes,
		# 'url': url,
		}
		return render(request, 'demo/home.django-html', context)


class DetailView(View):
	def get(self, request, slug, *args, **kwargs):
		product_or_service = Item.objects.get(slug=slug)
		context = {
			'product_or_service': product_or_service,
		}
		return render(request, 'demo/product-detail.django-html', context)