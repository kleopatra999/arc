# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2013-2014 Red Hat
# Author: Cleber Rosa <cleber@redhat.com>

"""
Module that implements the actions for the CLI App when the host toplevel
command is used
"""


import logging
import functools

import arc.cli.actions.base
import arc.host
import arc.shared.frontend


OBJ_NAME = "host"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.host.get_objs))


add = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.add_with_name,
                      OBJ_NAME, arc.host.add))


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete,
                      OBJ_NAME, arc.host.Host, arc.host.delete))


@arc.cli.actions.base.action
def list_jobs(app):
    """
    List host and jobs currently running on them

    :param app: the running application instance
    """
    def get_job_id_name(queue, host_id):
        for j in queue:
            if j['host']['id'] == host_id:
                return (j['job']['id'], j['job']['name'])
        return ('', '')

    line_fmt = "%-6s%-34s%-8s%-80s"
    header = line_fmt % ("ID", "NAME", "JOB ID", "JOB NAME")
    header_printed = False
    queue = app.connection.run(arc.shared.frontend.AFE_SERVICE_NAME,
                               'get_host_queue_entries', active=True)
    hosts = arc.host.get_objs(app.connection)
    for h in hosts:
        if not header_printed:
            print(header)
            header_printed = True

        (job_id, job_name) = get_job_id_name(queue, h.identification)

        print(line_fmt % (h.identification,
                          h.name,
                          job_id,
                          job_name))


@arc.cli.actions.base.action
def lock(app):
    '''
    Locks the chosen host

    :param app: the running application instance
    '''
    identification = arc.cli.actions.base.get_identification(app)
    if identification is None:
        logging.error('No host identification (name or id given)')
        return

    arc.host.modify(app.connection, identification, locked=True)


@arc.cli.actions.base.action
def unlock(app):
    '''
    Unlocks the chosen host

    :param app: the running application instance
    '''
    identification = arc.cli.actions.base.get_identification(app)
    if identification is None:
        logging.error('No host identification (name or id given)')
        return

    arc.host.modify(app.connection, identification, locked=False)


@arc.cli.actions.base.action
def reverify(app):
    '''
    Schedules a reverification for the chosen host

    :param app: the running application instance
    '''
    if app.parsed_arguments.name:
        arc.host.reverify(app.connection,
                          app.parsed_arguments.name)
