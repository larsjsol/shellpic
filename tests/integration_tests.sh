#!/usr/bin/env bash
# -*- coding: utf-8; mode: Shell-script -*-

cd $(dirname $0)

TESTS=0
TESTS_OK=0

compare_output() {
    command=$1
    expected_output=$2
    tmpfile=workdir/tmp/$(basename $expected_output)
    
    TESTS=$((TESTS+1))

    /bin/echo -n "Comparing \"$command\" with $expected_output ... "
    eval $command > $tmpfile
    if diff $tmpfile $expected_output > /dev/null; 
    then
        echo "OK!"
        TESTS_OK=$((TESTS_OK+1))
        return 0
    else
        echo "Failed!"
        return 1
    fi
}

mkdir -p workdir/tmp

compare_output "shellpic --scale-x 20 --scale-y 20 --shell4 ../img/Lenna.png" "output/lenna_shell4.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --shell8 ../img/Lenna.png" "output/lenna_shell8.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --shell24 ../img/Lenna.png" "output/lenna_shell24.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --shell8 --animate ../img/imp.gif" "output/imp_anim_shell8.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --irc ../img/Lenna.png" "output/lenna_irc.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --nuts ../img/Lenna.png" "output/lenna_nuts.txt"
compare_output "shellpic --scale-x 20 --scale-y 20 --tinymux ../img/Lenna.png" "output/lenna_tinymux.txt"
# issue 6
compare_output "shellpic --scale-x 20 --scale-y 20 ../img/icon_thankyou.gif" "output/icon_thankyou.txt"
# issue 10
compare_output "cat ../img/Lenna.png | shellpic --scale-x 20 --scale-y 20 --shell8 -" "output/lenna_shell8.txt"

if ((TESTS_OK == TESTS))
then
    echo
    echo $TESTS_OK/$TESTS tests passed!
    echo
    true
else
    echo
    echo $((TESTS-TESTS_OK))/$TESTS tests failed!
    echo
    false
fi
    
