. Example assembly code from
. Chapter 1 page 19 fig 1.6a
. Modified to be a complete
. assembly program
INOUT   START       7F00
INLOOP  TD          INDEV       TEST INPUT DEVICE
        JEQ         INLOOP      LOOP UNTIL DEVICE IS READY
        RD          INDEV       READ ONE BYTE INTO REGISTER A
        STCH        DATA        STORE BYTE THAT WAS READ
        .
        .
        .
OUTLP   TD          OUTDEV      TEST OUTPUT DEVICE
        JEQ         OUTLP       LOOP UNTIL DEVICE IS READY
        LDCH        DATA        LOAD DATA BYTE INTO REGISTER A
        WD          OUTDEV      WRITE ONE BYTE TO OUTPUT DEVICE
        XOS
        .
        .
        .
INDEV   BYTE        X'F1'       INPUT DEVICE NUMBER
OUTDEV  BYTE        X'05'       OUTPUT DEVICE NUMBER
DATA    RESB        1           ONE-BYTE VARIABLE
        END