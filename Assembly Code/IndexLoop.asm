. Example assembly code from
. Chapter 1 page 17 fig 1.5a
. Modified to be a complete
. assembly program
XLOOP   START       7F00
        LDA         ZERO        INITIALIZE INDEX VALUE TO 0
        STA         INDEX
ADDLP   LDX         INDEX       LOAD INDEX VALUE INTO REGISTER X
        LDA         ALPHA,X     LOAD WORD FROM ALPHA INTO REGISTER A
        ADD         BETA,X      ADD WORD FROM BETA
        STA         GAMMA,X     STORE THE RESULT IN A WORD IN GAMMA
        LDA         INDEX       ADD 3 TO INDEX VALUE
        ADD         THREE
        STA         INDEX
        COMP        K300        COMPARE NEW INDEX VALUE TO 300
        JLT         ADDLP       LOOP IF INDEX IS LESS THAN 300
        XOS                     END PROGRAM AND EXIT TO THE OS
.
INDEX   RESW        1           ONE-WORD VARIABLE FOR INDEX VALUE
.                               ARRAY VARIABLES--100 WORDS EACH
ALPHA   WORD        24
        WORD        7
BETA    WORD        82
        WORD        53
GAMMA   RESW        10
.                               ONE_WORD CONSTANTS
ZERO    WORD        0
K300    WORD        6
THREE   WORD        3
        END