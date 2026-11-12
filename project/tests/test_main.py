import pytest

from project.src.main import Category, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_counters():
    """Обнуляет счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def phone1():
    return Smartphone("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")


@pytest.fixture
def phone2():
    return Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")


@pytest.fixture
def grass1():
    return LawnGrass("Газонная трава", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый")


@pytest.fixture
def grass2():
    return LawnGrass("Газонная трава 2", "Выносливая", 450.0, 15, "США", "5 дней", "Темно-зеленый")


# ---------- Старые тесты: Product, сеттер, new_product, Category ----------

def test_product_str():
    p = Product("Iphone 15", "512GB", 210000.0, 8)
    assert str(p) == "Iphone 15, 210000 руб. Остаток: 8 шт."


def test_price_setter_rejects_non_positive(capsys):
    p = Product("X", "d", 100.0, 1)
    p.price = 0
    assert p.price == 100.0
    assert "не должна" in capsys.readouterr().out


def test_price_decrease_confirmed(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p = Product("X", "d", 100.0, 1)
    p.price = 50.0
    assert p.price == 50.0


def test_price_decrease_rejected(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p = Product("X", "d", 100.0, 1)
    p.price = 50.0
    assert p.price == 100.0


def test_new_product_merges_duplicates():
    existing = [Product("Iphone 15", "d", 200.0, 2)]
    result = Product.new_product(
        {"name": "  iphone 15 ", "description": "d", "price": 220.0, "quantity": 3},
        existing,
    )
    assert result is existing[0]
    assert result.quantity == 5
    assert result.price == 220.0


def test_category_counters():
    Category("A", "d", [Product("X", "d", 1.0, 1)])
    assert Category.category_count == 1
    assert Category.product_count == 1


# ---------- Задание 1: наследование и атрибуты ----------

def test_smartphone_attributes(phone1):
    assert phone1.name == "Samsung Galaxy S23 Ultra"
    assert phone1.price == 180000.0
    assert phone1.efficiency == 95.5
    assert phone1.model == "S23 Ultra"
    assert phone1.memory == 256
    assert phone1.color == "Серый"


def test_lawn_grass_attributes(grass1):
    assert grass1.country == "Россия"
    assert grass1.germination_period == "7 дней"
    assert grass1.color == "Зеленый"


def test_inheritance():
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)


def test_inherited_price_setter_works(phone1, capsys):
    phone1.price = -1
    assert phone1.price == 180000.0
    assert "не должна" in capsys.readouterr().out


# ---------- Задание 2: сложение ----------

def test_add_same_class_smartphones(phone1, phone2):
    assert phone1 + phone2 == 180000.0 * 5 + 210000.0 * 8


def test_add_same_class_grass(grass1, grass2):
    assert grass1 + grass2 == 500.0 * 20 + 450.0 * 15


def test_add_different_classes_raises(phone1, grass1):
    with pytest.raises(TypeError):
        phone1 + grass1


def test_add_non_product_raises(phone1):
    with pytest.raises(TypeError):
        phone1 + 5


# ---------- Задание 3: добавление в категорию ----------

def test_add_product_accepts_subclasses(phone1, grass1):
    category = Category("Смесь", "описание", [])
    category.add_product(phone1)
    category.add_product(grass1)
    assert Category.product_count == 2


def test_add_product_rejects_non_product():
    category = Category("Пусто", "описание", [])
    with pytest.raises(TypeError):
        category.add_product("Not a product")
    assert Category.product_count == 0


def test_constructor_rejects_non_product():
    with pytest.raises(TypeError):
        Category("Ошибка", "описание", ["не товар"])