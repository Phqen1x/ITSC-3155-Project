from . import orders, order_details, recipes, menu_item, resources, customers, payment_information, promotions, \
     recipes_resources,categories

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    menu_item.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    payment_information.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    recipes_resources.Base.metadata.create_all(engine)
    categories.Base.metadata.create_all(engine)
