# Drives the test VM over QMP. Source it, then: q shot FILE | q type TEXT | q keys K1 K2*3 | q quit
q(){ ( cd "$(dirname "${BASH_SOURCE[0]}")" && python3 qmp.py qmp.sock "$@" ); }
