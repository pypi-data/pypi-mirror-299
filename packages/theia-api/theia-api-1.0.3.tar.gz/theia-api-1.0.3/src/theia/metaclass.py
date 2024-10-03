

import threading


class SingletonMetaCls(type):
    """
    单例元类
    """

    _instance_lock = threading.Lock()

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super().__init__(*args, **kwargs)


    def _init_instance(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)

        return cls._instance

    def __call__(cls, *args, **kwargs):
        reinit = kwargs.pop("reinit", None)
        instance = cls._init_instance(*args, **kwargs)
        if reinit:
            instance.__init__(*args, **kwargs)
        return instance

