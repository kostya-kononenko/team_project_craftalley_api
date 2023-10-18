from discount.models import Discount


def calculate_total_price_with_discount(cart):
    all_discount = Discount.objects.all()
    for discount in all_discount:
        if discount.name == cart.item.coupon:
            money_to_pay = (cart.item.price - (cart.item.price * discount.discount)) * cart.quantity
            return int(money_to_pay)

    money_to_pay = int(cart.item.price) * cart.quantity

    return money_to_pay



