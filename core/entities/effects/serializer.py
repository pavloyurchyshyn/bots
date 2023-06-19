import base64
import pickle
from global_obj.main import Global
from core.entities.effects.base import BaseEffect


def serialize_effect(effect: BaseEffect) -> str:
    return base64.b64encode(pickle.dumps(effect)).decode('utf-8')


def deserialize_effect(effect: str) -> BaseEffect:
    return pickle.loads(base64.b64decode(effect.encode('utf-8')))
