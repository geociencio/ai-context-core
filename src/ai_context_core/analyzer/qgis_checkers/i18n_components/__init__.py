"""I18n components package."""

from .string_utils import is_translatable_string
from .call_handlers import handle_i18n_call

__all__ = ["is_translatable_string", "handle_i18n_call"]
