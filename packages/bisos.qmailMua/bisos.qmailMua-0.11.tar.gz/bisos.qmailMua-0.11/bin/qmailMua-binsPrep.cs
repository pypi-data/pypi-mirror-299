#!/usr/bin/env python

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/binsprep/py3/bin/exmpl-binsPerp.cs
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

from bisos import b
from bisos.b import cs
from bisos.b import b_io

from bisos.qmail import qmail_binsPrep

cs.csuList_importedModules(['bisos.qmail.qmail_binsPrep'])


from bisos.binsprep import binsprep
ap = binsprep.aptPkg

def notqmailInstall():
    print("Example of Installation")

aptPkgsList = [
    ap("notqmail"),
    ap("notExample", func=notqmailInstall),
    ap("remoteReplace", func=qmail_binsPrep.qmailRemoteReplace().pyCmnd),
]

binsprep.setup(
    aptPkgsList=aptPkgsList,
    examplesHook=qmail_binsPrep.examples_csu,
)

####+BEGIN: b:py3:cs/seed :derived "binsprep" :origin "pipx"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  seed       [[elisp:(outline-show-subtree+toggle)][||]] <<binsprep>> <<pipx>>   [[elisp:(org-cycle)][| ]]
#+end_org """

__file__ = '/bisos/git/bxRepos/bisos-pip/binsprep/py3/bin/seedBinsPrep.cs'
with open(__file__) as f:
    exec(compile(f.read(), __file__, 'exec'))

####+END:
