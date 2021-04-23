class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = request.session.get('cart')
        if(not cart):
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, productid, price, quantity=1):
        if(quantity == 0):
            self.remove(productid)
            return
        self.cart[productid] = {'quantity': quantity, 'price': price}
        self.save()

    def remove(self, productid):
        if(productid in self.cart):
            del self.cart[productid]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(i['quantity']*i['price'] for i in self.cart.values())

    def __len__(self):
        return sum(i['quantity'] for i in self.cart.values())

    def empty(self):
        return len(self.cart) == 0

    def clear(self):
        del self.session['cart']

    def keys(self):
        return map(lambda k: int(k), self.cart.keys())

    def __getitem__(self, arg):
        if isinstance(arg, str):
            return self.cart[arg]['quantity']
        raise TypeError('Slicing cart is not allowed.')


def cart_preprocessor(request):
    return {'cart': Cart(request)}
