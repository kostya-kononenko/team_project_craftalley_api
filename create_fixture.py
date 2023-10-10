def main():
    fake: Faker = Faker()
    for _ in range(50):
        User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            about_myself=fake.sentence(),
            city=fake.city(),
            email=fake.email(),
            password=fake.password(),
            date_of_birth=fake.date()
        )
        print(f"Created users. Name: {User.first_name} - {User.last_name}")

    user_count = User.objects.count()

    print(f"There are {user_count} in the database")

    for _ in range(20):
        Catalog.objects.create(
           name=fake.word(),
        )
        print(f"Created catalog. Name: {Catalog.name}")

    catalog_count = Catalog.objects.count()

    print(f"There are {catalog_count} in the database")


    catalog = Catalog.objects.all()


    for _ in range(40):
        Category.objects.create(
           name=fake.word(),
            catalog=random.choice(catalog)
        )
        print(f"Created category. Name: {Category.name}")

    category_count = Category.objects.count()

    print(f"There are {category_count} in the database")

    category = Category.objects.all()
    users = User.objects.all()

    for _ in range(500):
        Product.objects.create(
            name=fake.word(),
            description=fake.paragraph(nb_sentences=5),
            characteristics=fake.paragraph(nb_sentences=5),
            delivery=random.choices(["Ukrposhta", "Novaposhta", "Сourier", "Pickup"], [25, 25, 25, 25])[0],
            return_conditions=fake.paragraph(nb_sentences=5),
            price=random.randint(10, 10000),
            coupon=fake.word(),
            quantity=random.randint(10, 100),
            category=random.choice(category),
            manufacturer=random.choice(users),

        )
        print(f"Created product. Name: {Product.name}")

    product_count = Product.objects.count()

    print(f"There are {product_count} in the database")


if __name__ == "__main__":
    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "craftalley_api.settings")
    application = get_wsgi_application()

    import random

    from faker import Faker
    from user.models import User
    from product.models import Catalog, Category, Product

    main()
