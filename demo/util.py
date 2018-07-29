import importlib


def import_class(path):
    module_path, class_name = path.rsplit('.', maxsplit=1)
    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    return class_
