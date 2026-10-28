import pytest

from project.src.main import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def products() -> list[Product]:
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]


def test_product_init(products: list[Product]) -> None:
    p = products[0]
    assert (p.name, p.description, p.price, p.quantity) == (
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )


def test_category_init(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    assert c.name == "Смартфоны"
    assert c.description == "Описание"
    assert c.products == products


def test_counters_accumulate(products: list[Product]) -> None:
    Category("Смартфоны", "Описание", products)
    Category("Телевизоры", "Описание", [Product('55" QLED 4K', "Подсветка", 123000.0, 7)])
    assert Category.category_count == 2
    assert Category.product_count == 4


def test_counters_use_list_length_not_quantity(products: list[Product]) -> None:
    Category("Одна", "Описание", [products[0]])  # quantity = 5, но считается 1
    assert Category.product_count == 1


def test_counters_are_class_attributes(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    assert c.category_count == Category.category_count == 1
    assert "category_count" not in c.__dict__