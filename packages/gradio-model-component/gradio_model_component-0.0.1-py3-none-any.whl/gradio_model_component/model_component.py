from __future__ import annotations

from gradio_client.documentation import document, set_documentation_group

from gradio.blocks import BlockContext
from gradio.context import Context
from gradio.component_meta import ComponentMeta
from gradio.events import Events

set_documentation_group("layout")


@document()
class model_component(BlockContext, metaclass=ComponentMeta):
    EVENTS = [Events.blur]

    def __init__(
        self,
        *,
        visible: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        allow_user_close: bool = True,
        render: bool = True,
        close_on_esc: bool = True,
        close_outer_click: bool = True,
        close_message: str | None = None,
        bg_blur: int | None = 4,
        width: int | None = None,
        height: int | None = None,

    ):
        """
        Parameters:
            visible: If False, modal will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional string or list of strings that are assigned as the class of this component in the HTML DOM. Can be used for targeting CSS styles.
            allow_user_close: If True, user can close the modal (by clicking outside, clicking the X, or the escape key).
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            close_on_esc: If True, allows closing the modal with the escape key. Defaults to True.
            close_outer_click: If True, allows closing the modal by clicking outside. Defaults to True.
            close_message: The message to show when the user tries to close the modal. Defaults to None.
            bg_blur: The percentage of background blur. Should be a float between 0 and 1. Defaults to None.
            width: Modify the width of the modal.
            height: Modify the height of the modal.
        """
        self.allow_user_close = allow_user_close
        self.close_on_esc = close_on_esc
        self.close_outer_click = close_outer_click
        self.close_message = close_message
        self.bg_blur = bg_blur
        self.width = width
        self.height = height

        # Pass only the parameters that BlockContext expects
        BlockContext.__init__(
            self,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
        )

        if Context.root_block:
            self.blur(
                None,
                None,
                self,
                js="""
                () => {
                    return {
                        "__type__": "update",
                        "visible": false
                    }
                }
                """
            )
