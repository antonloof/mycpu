.origin #0

    ST R0 #10
loop:
    ADD R0 #1
    BR R0 != #100 loop
    HLT

