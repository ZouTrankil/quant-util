import json
import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, int):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class IntEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def int2str(json_data):
    correctedDict = {}
    for key, value in json_data.items():
        isError = False
        if (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool):
            value = str(value)
        elif isinstance(value, object):
            try:
                value = value.__dict__
            except Exception as e:
                isError = True
                pass
        if isError:
            if isinstance(value, list):
                value = [int2str(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                value = int2str(value)
        correctedDict[key] = value
    return correctedDict


class JsonUtil(object):
    @staticmethod
    def serialize(obj, indent = 1):
        if obj:
            return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=indent)
        return ''

    @staticmethod
    def serializeIntToStr(obj: dict, indent = 1):
        if obj:
            obj = int2str(JsonUtil.deserialize(JsonUtil.serialize(obj)))
            return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=indent, cls=IntEncoder)
        return ''

    @staticmethod
    def deserialize(jsonStr):
        return json.loads(jsonStr)


if __name__ == '__main__':
    print(JsonUtil.serializeIntToStr({'a': 123123123123123}))
