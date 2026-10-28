# Product & Category

Небольшой учебный проект на Python: два класса для описания товаров и категорий магазина, а также тесты к ним.

## Описание

Проект содержит два класса:

- **`Product`** — товар. Хранит название, описание, цену и количество в наличии.
- **`Category`** — категория товаров. Хранит название, описание и список товаров. Дополнительно ведёт общую статистику по всем созданным категориям.

### Атрибуты

| Класс      | Атрибут          | Тип             | Описание                                      |
|------------|------------------|-----------------|-----------------------------------------------|
| `Product`  | `name`           | `str`           | Название товара                               |
| `Product`  | `description`    | `str`           | Описание товара                               |
| `Product`  | `price`          | `float`         | Цена                                          |
| `Product`  | `quantity`       | `int`           | Количество в наличии                          |
| `Category` | `name`           | `str`           | Название категории                            |
| `Category` | `description`    | `str`           | Описание категории                            |
| `Category` | `products`       | `list[Product]` | Список товаров категории                      |
| `Category` | `category_count` | `ClassVar[int]` | Общее количество категорий (атрибут класса)   |
| `Category` | `product_count`  | `ClassVar[int]` | Общее количество товаров (атрибут класса)     |

Счётчики `category_count` и `product_count` обновляются автоматически при создании нового объекта `Category`. Количество товаров считается как длина списка `products`, а не как сумма `quantity`.

## Требования

- Python 3.10+
- pytest (для запуска тестов)

## Установка

```bash
git clone <ссылка-на-репозиторий>
cd <папка-проекта>
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install pytest
```

## Пример использования

```python
from models import Category, Product

phone = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
tv = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

phones = Category("Смартфоны", "Описание смартфонов", [phone])
tvs = Category("Телевизоры", "Описание телевизоров", [tv])

print(Category.category_count)  # 2
print(Category.product_count)   # 2
```

## Тесты

```bash
pytest -v
```

Тесты проверяют:

- корректную инициализацию `Product` и `Category`;
- накопление счётчиков при создании нескольких категорий;
- подсчёт товаров по длине списка, а не по `quantity`;
- что счётчики хранятся в классе, а не в экземпляре.

## Структура проекта

```
.
├── models.py        # классы Product и Category
├── test_models.py   # тесты на pytest
└── README.md
```