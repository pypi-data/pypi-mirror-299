import logging
from logging.handlers import RotatingFileHandler
from os.path import abspath, join, dirname
from typing import Optional

import panel as pn
from atap_corpus.corpus.corpus import DataFrameCorpus
from atap_corpus_loader import CorpusLoader
from panel import Row
from panel.widgets import Tqdm, Button, TextInput, Select, IntInput


class CorpusExtractor(pn.viewable.Viewer):
    """
    A tool for extracting the context around searched text in a corpus
    """
    LOGGER_NAME: str = "corpus-extractor"
    
    CONTEXT_TYPES: list[str] = ['characters', 'words', 'sentences', 'paragraphs']

    @staticmethod
    def setup_logger(logger_name: str, run_logger: bool):
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        if not run_logger:
            logger.addHandler(logging.NullHandler())
            return

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)6s - %(name)s:%(lineno)4d %(funcName)20s() - %(message)s')
        log_file_location = abspath(join(dirname(__file__), '..', 'log.txt'))
        # Max size is ~10MB with 1 backup, so a max size of ~20MB for log files
        max_bytes: int = 10000000
        backup_count: int = 1
        file_handler = RotatingFileHandler(log_file_location, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        logger.info('Logger started')

    @staticmethod
    def log(msg: str, level: int):
        logger = logging.getLogger(CorpusExtractor.LOGGER_NAME)
        logger.log(level, msg)

    def __init__(self,
                 corpus_loader: Optional[CorpusLoader] = None,
                 run_logger: bool = False,
                 **params):
        """
        CorpusExtractor constructor
        :param corpus_loader: The CorpusLoader that the extractor will be attached to. If None, a default CorpusLoader will be created with no optional features. None by Default.
        :type corpus_loader: Optional[CorpusLoader]
        :param run_logger: If True, a log file will be written to. False by default.
        :type run_logger: bool
        """
        super().__init__(**params)

        CorpusExtractor.setup_logger(CorpusExtractor.LOGGER_NAME, run_logger)

        self.progress_bar = Tqdm(visible=False)
        self.corpus_selector = Select(name='Selected corpus')

        self.context_count_input = IntInput(name='Context count', value=10, start=0)
        self.context_type = Select(name='Context type', options=CorpusExtractor.CONTEXT_TYPES)

        self.extract_corpus_button = Button(
            name="Extract",
            button_type="success", button_style="solid",
            height=30, width=100,
            visible=False,
            align="end"
        )
        self.extract_corpus_button.on_click(self.extract_corpus)

        self.name_field = TextInput(name='Name', placeholder='Enter a name (leave blank to autogenerate)',
                                    visible=False)

        self.extractor_panel = pn.Column(height=500)
        self._update_display()

        if corpus_loader:
            self.corpus_loader: CorpusLoader = corpus_loader
        else:
            self.corpus_loader: CorpusLoader = CorpusLoader(root_directory='.', run_logger=run_logger)
        self.corpora = self.corpus_loader.get_mutable_corpora()

        self.corpus_loader.register_event_callback("build", self._on_corpora_update)
        self.corpus_loader.register_event_callback("rename", self._on_corpora_update)
        self.corpus_loader.register_event_callback("delete", self._on_corpora_update)
        self.corpus_loader.add_tab("Corpus Extractor", self.extractor_panel)
        self._on_corpora_update()

    def __panel__(self):
        return self.corpus_loader

    def get_corpus_loader(self) -> CorpusLoader:
        return self.corpus_loader

    def get_mutable_corpora(self) -> DataFrameCorpus:
        return self.corpora

    def display_error(self, error_msg: str):
        self.log(f"Error displayed: {error_msg}", logging.DEBUG)
        pn.state.notifications.error(error_msg, duration=0)

    def display_success(self, success_msg: str):
        self.log(f"Success displayed: {success_msg}", logging.DEBUG)
        pn.state.notifications.success(success_msg, duration=3000)

    def _update_display(self, *_):
        panel_objects = []
        panel_objects.extend([
            self.progress_bar,
            Row(),
            Row(self.extract_corpus_button, self.name_field)
        ])
        self.extractor_panel.objects = panel_objects

    def _on_corpora_update(self, corpus=None, *_):
        if self.corpus_loader is None:
            return

        formatted_dict: dict[str, DataFrameCorpus] = {}
        for corpus in self.corpora.items():
            label = f"{corpus.name} | docs: {len(corpus)}"
            if corpus.parent:
                label += f" | parent: {corpus.parent.name}"
            formatted_dict[label] = corpus
        self.corpus_selector.options = formatted_dict

        corpus_exists = bool(len(formatted_dict))
        if corpus_exists:
            self.corpus_selector.value = list(formatted_dict.values())[-1]
        else:
            self.corpus_selector.value = None

        self.corpus_selector.visible = corpus_exists
        self.corpus_selector.visible = corpus_exists

    def extract_corpus(self, *_):
        new_name = self.name_field.value_input
