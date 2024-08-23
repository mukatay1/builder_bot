import pkgutil
import importlib

from aiogram import Dispatcher, Router


def register_routers_from_package(package_name: str, dp: Dispatcher) -> None:
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Router):
                dp.include_router(attr)