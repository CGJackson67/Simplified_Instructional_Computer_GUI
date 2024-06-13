. Based on example assembly code from
. Chapter 2 page 111 exercise 2
. Tests our custom opcode: XOS and TIXW
SUMCUS  START       4000
FIRST   LDX         ZERO
        LDA         ONE
LOOP1   MUL         COUNT
        STA         TABLE,X
        TIXW         COUNT
        JLT         LOOP1
        LDX         ZERO
        LDA         ZERO
LOOP2   ADD         TABLE,X
        TIXW         COUNT
        JLT         LOOP2
        STA         TOTAL
        XOS
TABLE   RESW        2000
COUNT   WORD        3
ZERO    WORD        0
ONE     WORD        1
TOTAL   RESW        1
        END         FIRST