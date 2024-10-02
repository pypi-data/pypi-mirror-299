from .layout import Layout
from .models.command import Command
from .module import Module
from .templater import Templater, TemplateType


class CommandCreator:
    """Class for creating 'command' entrypoints, which run an executable on a path."""

    def __init__(self, templater: Templater, layout: Layout) -> None:
        self._templater = templater
        self._entrypoints_root = layout.entrypoints_root

    def create_entrypoint_file(
        self,
        config: Command,
        module: Module,
    ) -> None:
        entrypoints_folder = (
            self._entrypoints_root / module.metadata.name / module.metadata.version
        )
        entrypoints_folder.mkdir(parents=True, exist_ok=True)
        entrypoint_file = entrypoints_folder / config.name

        params = {
            "command_path": config.command_path,
            "command_args": config.command_args,
        }

        self._templater.create(
            entrypoint_file, TemplateType.COMMAND_ENTRYPOINT, params, executable=True
        )
