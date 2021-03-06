
__copyright__ = """
Copyright (C) 2005, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys, os
from stgit.argparse import opt
from stgit.commands.common import *
from stgit.utils import *
from stgit import argparse, stack, git

help = 'Show the tree status'
kind = 'wc'
usage = ['[options] [--] [<files or dirs>]']
description = """
Show the status of the whole working copy or the given files. The
command also shows the files in the current directory which are not
under revision control. The files are prefixed as follows:

  M - locally modified
  N - newly added to the repository
  D - deleted from the repository
  C - conflict
  ? - unknown

An 'stg refresh' command clears the status of the modified, new and
deleted files."""

args = [argparse.files]
options = [
    opt('-m', '--modified', action = 'store_true',
        short = 'Show modified files only'),
    opt('-n', '--new', action = 'store_true',
        short = 'Show new files only'),
    opt('-d', '--deleted', action = 'store_true',
        short = 'Show deleted files only'),
    opt('-c', '--conflict', action = 'store_true',
        short = 'Show conflict files only'),
    opt('-u', '--unknown', action = 'store_true',
        short = 'Show unknown files only'),
    opt('-x', '--noexclude', action = 'store_true',
        short = 'Do not exclude any files from listing'),
    opt('--reset', action = 'store_true',
        short = 'Reset the current tree changes')]

directory = DirectoryHasRepository(needs_current_series = False, log = False)

def status(files, modified, new, deleted, conflict, unknown, noexclude):
    """Show the tree status
    """
    cache_files = git.tree_status(files,
                                  unknown = (not files),
                                  noexclude = noexclude)
    filtered = (modified or new or deleted or conflict or unknown)

    if filtered:
        filestat = []
        if modified:
            filestat.append('M')
        if new:
            filestat.append('A')
            filestat.append('N')
        if deleted:
            filestat.append('D')
        if conflict:
            filestat.append('C')
        if unknown:
            filestat.append('?')
        cache_files = [x for x in cache_files if x[0] in filestat]

    output = []
    for st, fn in cache_files:
        if filtered:
            output.append(fn)
        else:
            output.append('%s %s' % (st, fn))
    for o in sorted(output):
        out.stdout(o)

def func(parser, options, args):
    """Show the tree status
    """
    args = git.ls_files(args)
    directory.cd_to_topdir()

    if options.reset:
        directory.log = True
        if args:
            conflicts = git.get_conflicts()
            git.resolved([fn for fn in args if fn in conflicts])
            git.reset(args)
        else:
            resolved_all()
            git.reset()
    else:
        status(args, options.modified, options.new, options.deleted,
               options.conflict, options.unknown, options.noexclude)
