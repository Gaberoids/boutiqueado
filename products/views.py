from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# Q = is important for searches, instead of returning resuts for where the terms or found in all fields, it returns if the term is found in either fields
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

from .forms import ProductForm

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # to avoid getting error for running the code without a search term
    query = None
    categories = None
    sort = None
    direction = None

# this if is for the "Clothing" menu item
    if request.GET:
        print('all_product function inside the request.GET if ---------***********-----------------**************------------')
        if 'sort' in request.GET:
            print('all_product function - inside the request.GET if sort in these ---------***********-----------------**************------------')
            sortkey = request.GET['sort']
            print(str(sortkey) + ' = value of sortkey in string format ---------***********-----------------**************------------')
            sort = sortkey
            print(sort + '= print sort app_product function ---------***********-----------------**************------------')

            #  to make sorting case insensitive, we have to create a temporary
            # ...field called lower.
            if sortkey == 'name':
                sortkey = 'lower_name'
                print(str(sortkey) + ' = under sort key = name ---------***********-----------------**************------------')
                products = products.annotate(lower_name=Lower('name'))
                print(products)
                print(lower_name)

            if sortkey == 'category':
                sortkey = 'category__name'  # double underline allow driling
                # ... into a model

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            # the below variable put all categories on a list splitted
            # ... via comma
            categories = request.GET['category'].split(',')
            # the below variable filter products based the category
            products = products.filter(category__name__in=categories)
            # the double underline above means grab category names with
            # ... category=categorynamefrom list above
            # below, variable contain a list of all categories . Since it is
            # ... an object, we can access the category fields from the template
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn;t enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            # icontains = i means case insensitive
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    print(product_id + '  = product_id ---------***********-----------------**************------------')
    product = get_object_or_404(Product, pk=product_id)
    print(product)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        # the request.files is to get images
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        # add an instance of a form
        form = ProductForm()
    print("product/views.py > add_product > form instance ---------***********-----------------**************------------")
    print(form)
    print(" end of form instance ---------***********-----------------**************------------")
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        print("edit_product -> product = ---------***********-----------------**************------------")
        print(product)
        print('product end')
        print("edit_product form = ---------***********-----------------**************------------")
        print(form)
        print('form end')

        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
