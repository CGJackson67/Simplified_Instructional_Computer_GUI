. Example assembly code from
. Chapter 1 page 20 fig 1.7a
. Modified to be a complete
. assembly program
SUBRT   START       7F00
        JSUB        READ        CALL READ SUBROUTINE
        XOS
        .
        .
        .                       SUBROUTINE TO READ 100-BYTE RECORD
READ    LDX         ZERO        INITIALIZE INDEX REGISTER TO 0
RLOOP   TD          INDEV       TEST INPUT DEVICE
        JEQ         RLOOP       LOOP IF DEVICE IS BUSY
        RD          INDEV       READ ONE BYTE INTO REGISTER A
        STCH        RECORD,X    STORE DATA BYTE INTO RECORD
        TIX         K100        ADD 1 TO INDEX AND COMPARE TO K100
        JLT         RLOOP       LOOP IF INDEX IS LESS THAN K100
        RSUB                    EXIT FROM SUBROUTINE
        .
        .
        .
INDEV   BYTE        X'F1'       INPUT DEVICE NUMBER
RECORD  RESB        100         100-BYTE BUFFER FOR INPUT RECORD
        .                       ONE WORD CONSTANTS
ZERO    WORD        0
K100    WORD        3
        END