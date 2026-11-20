# Ansible Role: doas

This role installs and configures doas.

## Requirements

Requires ansible-core 2.18 or later.

One of the supported operating systems/distributions:

* Debian
* FreeBSD
* OpenBSD

Gather facts before running the role, and run with sufficient privileges to
install packages and manage the doas configuration file.

## Role Variables

Here's a list of the available variables and their default values (see `defaults/main.yml`).

    doas_config_file: /etc/doas.conf

Full path to the doas configuration file. The default value depends on the
target platform (FreeBSD keeps the doas configuration in /usr/local/etc/doas.conf, for example).

    doas_config_file_mode: "0600"
    
File permissions for doas config. 

    doas_config_owner: root
    doas_config_group: wheel

User and group owner of config.

    doas_package: doas

Doas package name.

    doas_sudo_package: sudo
    doas_remove_sudo: false

Name of sudo package and whether to ensure it's not installed.

When removal is enabled, the role refuses to proceed if its effective privilege
escalation settings use sudo. Connect as root with become disabled, or use
another become method. This guard checks current sudo dependence; it does not
verify replacement administrative access or the settings of future playbooks.

    doas_all_config: []
    doas_group_config: []
    doas_host_config: []

These lists contain the actual doas.conf rules. Place `doas_all_config`
in your `group_vars/all` to apply them to all hosts running this role. 
`doas_group_config` is used to apply doas rules on the group level. 


One could, for example, use the following configuration in `group_vars/openbsd`
to be able to run `syspatch` and `pkg_add -u` without a password:

    doas_group_config:
      - action: permit
        options:
          - nopass
        identity: your_username
        as: root
        cmd: syspatch
      - action: permit
        options:
          - nopass
        identity: your_username
        as: root
        cmd: pkg_add
        args: -u

Lastly, use `doas_host_config` to add rules for a specific host.

The main role manages these lists in one block named `inventory`, in all, group,
then host order. Rules retain their order within each list. Content outside the
block is preserved. When all three lists are empty, only the inventory block is
removed. Do not edit managed blocks manually; changes inside them are replaced
on the next application.

## Role-Owned Rules

Other roles and playbooks can call the `rules` entry point to manage their own
named blocks without adding rules to the inventory lists. Install doas first,
normally by running the main role. The `rules` entry point loads platform settings
but does not install packages or remove sudo.

For example, after installing borgmatic and creating its user:

```yaml
- name: Allow borgmatic to run as root
  ansible.builtin.include_role:
    name: sjktje.doas
    tasks_from: rules
  vars:
    doas_rules_name: borgmatic backup privileges
    doas_rules:
      - action: permit
        options: [nopass]
        identity: borgmatic
        as: root
        cmd: /usr/bin/borgmatic
```

Use the actual installed command path on the target host. Running borgmatic as
root may grant broad root access if the invoking user can modify its configuration
or select configuration containing command hooks. Review configuration ownership
and permitted arguments as part of granting this access.

| Variable | Meaning |
| --- | --- |
| `doas_rules_name` | Required, stable name identifying one block. |
| `doas_rules_state` | `present` (default) or `absent`. |
| `doas_rules` | Non-empty list of rules, required for `present`. |

Names may contain spaces and punctuation, but must not be blank or contain line
breaks, control characters or the literal `{mark}`. Names must be unique within
the configuration file. The name `inventory` is reserved for the main role.
Renaming creates a different block; remove the old name explicitly.

Each rule requires `action` (`permit` or `deny`) and a non-empty string `identity`.
Prefix group identities with `:`, and quote numeric identities. Optional fields
are `options` (a list), `as`, `cmd` and `args`. Command and argument values are
rendered as doas syntax; YAML quoting alone does not quote arguments for doas.
Omitting `args` leaves arguments unrestricted, whereas `args: ""` requires the
command to run without arguments. Omitting `as` allows any target user.

The entry point honours the existing configuration path, ownership and mode
variables. It manages the complete contents of the named block and validates the
whole candidate file with `doas -C` before applying changes. Validation checks
syntax, not whether the resulting permissions are appropriate or sufficient.

To remove a block, supply its name and `absent`; no rules are needed:

```yaml
- name: Remove borgmatic privileges
  ansible.builtin.include_role:
    name: sjktje.doas
    tasks_from: rules
  vars:
    doas_rules_name: borgmatic backup privileges
    doas_rules_state: absent
```

Removing an already absent block is a no-op, including when the configuration
file is missing. Removing a role from a playbook does not remove its old rules;
run an explicit removal task when retiring them.

## Rule Ordering

New blocks append to the configuration file. Updating an existing block keeps
its position, so block order depends on creation history, not current role
execution order.

Doas uses the **last matching rule**. A later permit can override an earlier deny,
including across managed blocks and manually maintained rules. This role does
not centrally enforce ordering across blocks. Keep overlapping rules together
when their ordering is security-critical. Avoid concurrent playbook runs that
write the same configuration file.

## Migration

Versions prior to 2.0.0 replaced the whole configuration file. If you are upgrading
from one of those versions to 2.0.0 or later, follow the migration steps below.
Those versions did not mark the rules they generated, so this role cannot safely
distinguish those rules from manual additions. Existing unmarked entries are
preserved, not adopted or removed automatically.

1. Back up and review the existing configuration. Keep a root session or another
   working administrative route available throughout migration.
2. Identify the old role-generated rules and ensure their intended replacements
   are present in the inventory lists or role-owned rulesets.
3. Apply the updated role to create the managed blocks, then remove the old
   unmarked role-generated entries, preserving genuine manual rules. Review rule
   ordering while both old and new entries exist.
4. Validate the resulting file with `doas -C /path/to/doas.conf` and verify the
   intended administrative access before closing the fallback session.

Do not enable `doas_remove_sudo` until replacement administrative access is
verified. Removing sudo can break subsequent tasks and future runs if Ansible
still uses sudo for privilege escalation.

Example Playbook
----------------

For example, configure selected maintenance commands on OpenBSD hosts:

    - hosts: servers
      user: root
      vars:
        doas_host_config:
          - action: permit
            options:
              - nopass
            identity: your_username
            as: root
            cmd: syspatch
          - action: permit
            options:
              - nopass
            identity: your_username
            as: root
            cmd: pkg_add
            args: -u
      roles:
         - { role: sjktje.doas }

License
-------

BSD
