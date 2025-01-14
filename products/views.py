from django.shortcuts import render, redirect

from products.handler import bot
from products.models import ProductModel, CategoryModel, CartModel


def home_page(request):
    products = ProductModel.objects.all()
    categories = CategoryModel.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'index.html', context=context)

def not_fount_page(request):
    return render(request, 'notfound.html')

def search(request):
    # Пользотватель отправляет Iphone12
    if request.method == 'POST':
        # {'search_product': Iphone12 }
        get_product = request.POST.get('search_product')
        try:
            exact_product = ProductModel.objects.get(product_name__icontains=get_product)
            return redirect(f'/products/{exact_product.id}')
        except:
            return redirect('notfound')

# Страница определенного продукта
def product_page(request, id):
    product = ProductModel.objects.get(id=id)
    context = {'product': product}
    return render(request, 'single-product.html', context=context)


def about_page(request):
    return render(request, 'about.html')


# Функция для добавления товара в корзину
def add_product_to_cart(request, id): #3
    if request.method == 'POST':
        print('THis is post')
        checker = ProductModel.objects.get(id=id)  #3 10
        if checker.count >= int(request.POST.get('pr_count')): #12
            CartModel.objects.create(user_id=request.user.id, user_product=checker,
                                     user_product_quantity=int(request.POST.get('pr_count')))
            print('SUCCESS')
            return redirect('/user_cart')
        else:
            print('ERROR')
            return redirect('/')

# Корзина самого пользователя
def user_cart(request):
    cart = CartModel.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        main_text = 'Новый заказ ока!'

        for i in cart:
            main_text += f'\n Товар: {i.user_product}\n' \
                         f'\n Кол-во: {i.user_product_quantity}\n' \
                         f'\n ID пользователя: {i.user_id}\n' \
                         f'\n Цена: {i.user_product.price}\n'
            bot.send_message(-1002195311609, main_text)
            cart.delete()
            return redirect('/')
    else:
        return render(request, 'cart.html', context={'cart': cart})