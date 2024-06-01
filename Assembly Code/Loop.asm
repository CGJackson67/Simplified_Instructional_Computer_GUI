. Example assembly code from
. Chapter 1 page 16 fig 1.4a
. Modified to be a complete
. assembly program
LOOP    START       7F00
        LDX         ZERO        INITIALIZE INDEX REGISTER TO 0
MOVECH  LDCH        STR1,X      LOAD CHARACTER FROM STR1 INTO REG A
        STCH        STR2,X      STORE CHARACTERS INTO STR2
        TIXB        ELEVEN      ADD 1 TO INDEX, COMPARE RESULT TO 11
        JLT         MOVECH      LOOP IF INDEX IS LESS THAN 11
        XOS                     END PROGRAM AND EXIT TO THE OS
.
STR1    BYTE        C' E T ST  NG'      11-BYTE STRING CONSTANT
STR2    RESB        11                  11-BYTE VARIABLE
.                                       ONE-WORD CONSTANTS
ZERO    WORD        0
ELEVEN  WORD        11
        END