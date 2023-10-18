from product.models import Product


class FavoriteHelper:
    def __init__(self, user):
        self.user = user
        self.favorite_items = []
        self.checkout_details = {"products": [], }

    def prepare_favorite_for_checkout(self):
        self.favorite_items = Product.objects.filter(favorite__isnull=False)
        if not self.favorite_items:
            return False

        self.prepare_checkout_details()
        return self.checkout_details

    def prepare_checkout_details(self):
        for favorite_item in self.favorite_items:
            self.checkout_details["products"].append(
                {
                    "id": favorite_item.id,
                    "name": favorite_item.name,
                    "description": favorite_item.description,
                    "characteristics": favorite_item.characteristics,
                    "delivery": favorite_item.delivery,
                    "return_conditions": favorite_item.return_conditions,
                    "price": favorite_item.price,
                    "new_product": favorite_item.new_product,
                    "coupon": favorite_item.coupon,
                    "quantity": favorite_item.quantity,
                    "manufacturer": favorite_item.manufacturer.brand_name,
                    "category": favorite_item.category.name
                }
            )
