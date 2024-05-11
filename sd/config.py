"""
Load environment values
"""
from dotenv import load_dotenv

from common.core.envs import EnvSection

__all__ = [
    'env'
]

result = load_dotenv()


class EnvManager(object):
    django = EnvSection('django')
    rabbitmq = EnvSection('rabbitmq')
    redis = EnvSection('redis')


env = EnvManager()
