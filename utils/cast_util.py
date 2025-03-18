from functools import wraps


def bool(value):
    return value is True or str(value).lower() in ['yes', 'true', '1']


def camel_to_snake(camel_str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel_str]).lstrip('_')


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def adapt_fields(known_fields: set):
    """
    装饰器，用于将未知字段动态设置为对象的属性
    由于对接服务端战斗接口的时候，既有需要手动设置修改字段名的情况，也有需要动态设置属性的情况
    """

    def decorator(init_func):
        @wraps(init_func)
        def wrapper(self, content, *args, **kwargs):
            if content is None:
                content = {}

            # 调用原来的初始化方法
            init_func(self, content, *args, **kwargs)

            # 处理未知字段，动态设置为属性
            for key, value in content.items():
                if key not in known_fields:
                    # 如果值是None，直接设置为属性
                    if value is None:
                        setattr(self, camel_to_snake(key), value)
                    # 如果值是字典类型，递归处理
                    elif isinstance(value, dict):
                        setattr(self, camel_to_snake(key), {camel_to_snake(k): v for k, v in value.items()})
                    # 如果值是列表，递归处理每个元素
                    elif isinstance(value, list):
                        setattr(self, camel_to_snake(key), [adapt_object(v) for v in value])
                    else:
                        setattr(self, camel_to_snake(key), value)

        return wrapper

    return decorator


# 递归处理复杂类型
def adapt_object(value):
    if value is None:
        return None
    elif isinstance(value, dict):
        return {camel_to_snake(k): v for k, v in value.items()}
    elif isinstance(value, list):
        return [adapt_object(v) for v in value]
    else:
        return value
