# Ansible Role: doas

This role installs and configures doas.

## Requirements

One of the supported operating systems:

* OpenBSD
* FreeBSD


# Role Variables

Here's a list of the available variables and their default values (see `defaults/main.yml´).

    doas_config_file: /etc/doas.conf

Full path to the doas configuration file. The default value depends on the
target platform (FreeBSD keeps the doas configuration in /usr/local/etc/doas.conf, for example).

    doas_config_file_mode: 0600
    
File permissions for doas config. 

    doas_config_owner: root
    doas_config_group: wheel

User and group owner of config.

    doas_package: doas

Doas package name.

    doas_sudo_package: sudo
    doas_remove_sudo: false

Name of sudo package and whether to ensure it's not installed.

    doas_all_config: []
    doas_group_config: []
    doas_host_config: []

These dictionaries contain the actual doas.conf rules. Place `doas_all_config`
in your `group_vars/all` to apply them to all hosts running this role. 
`doas_group_config` is used to apply doas rules on the group level. 


One could, for example, use the following configuration is `group_vars/openbsd`
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


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      user: root
      vars:
        doas_remove_sudo: true
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
         - { role: sjk.doas }

License
-------

BSD
