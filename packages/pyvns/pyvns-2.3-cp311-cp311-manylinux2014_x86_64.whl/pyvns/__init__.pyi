from .vns_python_wrapper import Compiler as Compiler, Dialogue as Dialogue, DialoguesManager as DialoguesManager, Event as Event, Naming as Naming

dialogue_data_t = dict[str, str | list[str] | dict[str, str | list[dict[str, str]]] | list[dict[str, bool | int | float | str]]]
dialogue_section_t = dict[str, dialogue_data_t]
dialogue_content_t = dict[str, dialogue_section_t]
