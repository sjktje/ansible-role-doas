"""Check effective privilege escalation before removing sudo."""

from typing import Any

from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    """Reject sudo removal when the current task relies on sudo."""

    _requires_connection = False
    _supports_check_mode = True
    TRANSFERS_FILES = False

    def run(
        self,
        tmp: str | None = None,
        task_vars: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Check escalation without executing commands on the target.

        Parameters
        ----------
        tmp : str, optional
            Temporary path supplied by Ansible.
        task_vars : dict, optional
            Variables supplied by Ansible.

        Returns
        -------
        dict
            An unchanged result, marked failed if sudo is active.
        """
        result = super().run(tmp, task_vars)
        result["changed"] = False
        become_plugin = getattr(self._connection, "become", None)
        method = (
            become_plugin.name
            if become_plugin is not None
            else self._play_context.become_method
        )
        if boolean(self._play_context.become) and method.rsplit(".", 1)[-1] == "sudo":
            result["failed"] = True
            result["msg"] = (
                "Refusing to remove sudo while privilege escalation uses sudo. "
                "Disable become when connected as root, or use another become "
                "method before enabling doas_remove_sudo."
            )
        return result
