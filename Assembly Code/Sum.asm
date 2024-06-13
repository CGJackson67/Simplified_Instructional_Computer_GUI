. Example assembly code from
. Chapter 2 page 111 exercise 2
. Code will not work because the TABLE
. has no data, and TIX indexes bytes
. not integers (words)
SUM     START       4000
FIRST   LDX         ZERO
        LDA         ZERO
LOOP    ADD         TABLE,X
        TIX         COUNT
        JLT         LOOP
        STA         TOTAL
        RSUB
TABLE   RESW        2000
COUNT   RESW        1
ZERO    WORD        0
TOTAL   RESW        1
        END         FIRST