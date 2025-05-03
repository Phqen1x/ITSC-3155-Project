from . import (orders, order_details, resources, promotions, categories,
               recipes, menu_item)


def load_routes(app):
    # app.include_router(customers.router)
    # app.include_router(payment_information.router)
    app.include_router(orders.router)
    app.include_router(resources.router)
    app.include_router(promotions.router)
    app.include_router(categories.router)
    app.include_router(recipes.router)
    app.include_router(menu_item.router)
