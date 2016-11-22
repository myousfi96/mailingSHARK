import abc
import os
import sys
import logging


class BaseDataCollector(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def identifier(self):
        return

    def __init__(self, cfg, project_id):
        self.config = cfg
        self.project_id = project_id
        self.debug_level = logging.DEBUG

        if self.config is not None:
            self.debug_level = self.config.get_debug_level()

    @abc.abstractmethod
    def download_mail_boxes(self):
        pass

    @staticmethod
    def _import_backends():
        backend_files = [x[:-3] for x in os.listdir(os.path.dirname(os.path.realpath(__file__))) if x.endswith(".py")]
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        for backend in backend_files:
            __import__(backend)

    @staticmethod
    def find_fitting_backend(cfg, project_id):
        BaseDataCollector._import_backends()

        for sc in BaseDataCollector.__subclasses__():
            backend = sc(cfg, project_id)
            if backend.identifier == cfg.backend:
                return backend

        return None

    @staticmethod
    def get_all_possible_backend_options():
        BaseDataCollector._import_backends()

        choices = []
        for sc in BaseDataCollector.__subclasses__():
            backend = sc(None, None)
            choices.append(backend.identifier)
        return choices
