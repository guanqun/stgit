#!/bin/sh

test_description='Run "stg clean"'

. ./test-lib.sh

test_expect_success 'Initialize StGit stack' '
    stg init &&
    stg new e0 -m e0 &&
    stg new p0 -m p0 &&
    echo foo > foo.txt &&
    git add foo.txt &&
    stg refresh &&
    stg new e1 -m e1 &&
    stg new e2 -m e2 &&
    stg pop
'

test_expect_success 'Clean empty patches' '
    [ "$(echo $(stg applied))" = "e0 p0 e1" ] &&
    [ "$(echo $(stg unapplied))" = "e2" ] &&
    stg clean &&
    [ "$(echo $(stg applied))" = "p0" ] &&
    [ "$(echo $(stg unapplied))" = "" ]
'

test_done
