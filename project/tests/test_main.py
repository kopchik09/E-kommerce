import pytest

from project.src.main import BaseProduct, Category, Order, Product, ZeroQuantityError


def make_product(name="Тест", price=100.0, quantity=5):
    return Product(name, "описание", price, quantity)


# ---- Задание 1 ----

def test_zero_quantity_product_raises_value_error():
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Бракованный", "описание", 1000.0, 0)


def test_zero_quantity_error_is_value_error():
    assert issubclass(ZeroQuantityError, ValueError)


def test_base_product_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseProduct("name", "desc", 1.0, 1)


# ---- Задание 2 ----

def test_middle_price_average():
    category = Category("Тест", "описание", [
        make_product(price=100.0),
        make_product(price=200.0),
        make_product(price=300.0),
    ])
    assert category.middle_price() == pytest.approx(200.0)


def test_middle_price_empty_category_returns_zero():
    assert Category("Пустая", "описание", []).middle_price() == 0


# ---- Дополнительное задание ----

def test_add_zero_quantity_product_to_category_raises(capsys):
    product = make_product()
    product.quantity = 0  # через конструктор такой товар не создать
    category = Category("Тест", "описание", [])

    with pytest.raises(ZeroQuantityError):
        category.add_product(product)

    out = capsys.readouterr().out
    assert "Ошибка" in out
    assert "Обработка добавления товара завершена" in out
    assert "добавлен в категорию" not in out


def test_add_product_to_category_success_prints_messages(capsys):
    category = Category("Тест", "описание", [])
    category.add_product(make_product())

    out = capsys.readouterr().out
    assert "добавлен в категорию" in out
    assert "Обработка добавления товара завершена" in out


def test_order_with_zero_quantity_product_raises(capsys):
    product = make_product()
    product.quantity = 0

    with pytest.raises(ZeroQuantityError):
        Order(product, 1)

    out = capsys.readouterr().out
    assert "Ошибка" in out
    assert "Обработка добавления товара завершена" in out
    assert "добавлен в заказ" not in out


def test_order_success_prints_messages(capsys):
    Order(make_product(), 2)

    out = capsys.readouterr().out
    assert "добавлен в заказ" in out
    assert "Обработка добавления товара завершена" in out


def test_order_total_cost():
    order = Order(make_product(price=100.0, quantity=10), 3)
    assert order.total_cost == pytest.approx(300.0)


def test_order_more_than_stock_raises_value_error():
    with pytest.raises(ValueError):
        Order(make_product(quantity=2), 5)