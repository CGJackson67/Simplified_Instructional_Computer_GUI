. Example assembly code from
. Chapter 1 page 13 fig 1.2a
. Modified to be a complete
. assembly program
DATMOV  START       7F00
        LDA         FIVE        LOAD CONSTANT 5 INTO REGISTER A
        STA         ALPHA       STORE IN ALPHA
        LDCH        CHARZ       LOAD CHARACTER 'Z' INTO REGISTER A
        STCH        C1          STORE IN CHARACTER VARIABLE C1
        XOS                     END PROGRAM AND EXIT TO THE OS
ALPHA   RESW        1           ONE-WORD VARIABLE
FIVE    WORD        5           ONE-WORD CONSTANT
CHARZ   BYTE        C'Z'        ONE-BYTE CONSTANT
C1      RESB        1           ONE-BYTE VARIABLE
        END