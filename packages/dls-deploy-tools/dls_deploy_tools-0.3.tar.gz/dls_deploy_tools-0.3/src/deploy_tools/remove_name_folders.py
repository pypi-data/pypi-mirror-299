from pathlib import Path

from .layout import Layout
from .models.module import Module


class RemoveNameFoldersError(Exception):
    pass


def remove_name_folders(
    deprecated: list[Module],
    restored: list[Module],
    removed: list[Module],
    layout: Layout,
) -> None:
    """Remove module name folders where all versions have been removed."""
    for module in deprecated:
        delete_name_folder(module.metadata.name, layout.modulefiles_root)

    for module in restored:
        delete_name_folder(module.metadata.name, layout.deprecated_modulefiles_root)

    app_roots = layout.get_application_paths()
    for module in removed:
        delete_name_folder(module.metadata.name, layout.deprecated_modulefiles_root)

        for root in app_roots:
            delete_name_folder(module.metadata.name, root)


def delete_name_folder(name: str, area_root: Path) -> None:
    name_folder = area_root / name
    try:
        name_folder.rmdir()
    except OSError:
        pass
