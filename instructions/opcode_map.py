from instructions.comparisons import *
from instructions.constants import *
from instructions.conversions import *
from instructions.loads import *
from instructions.stores import *
from instructions.stack import *
from instructions.extend import *
from instructions.math import *
from instructions.references import *
from instructions.controls import *

opcode2instruction = {
    0x00: NOP(),
    0x01: ACONST_NULL(),
    0x02: ICONST_M1(),
    0x03: ICONST_0(),
    0x04: ICONST_1(),
    0x05: ICONST_2(),
    0x06: ICONST_3(),
    0x07: ICONST_4(),
    0x08: ICONST_5(),
    0x09: LCONST_0(),
    0x0a: LCONST_1(),
    0x0b: FCONST_0(),
    0x0c: FCONST_1(),
    0x0d: FCONST_2(),
    0x0e: DCONST_0(),
    0x0f: DCONST_1(),
    0x10: BIPUSH(),
    0x11: SIPUSH(),
    0x12: LDC(),
    0x13: LDC_W(),
    0x14: LDC2_W(),
    0x15: ILOAD(),
    0x16: LLOAD(),
    0x17: ILOAD(),  # FLOAD
    0x18: DLOAD(),
    0x19: ILOAD(),  # ALOAD
    0x1a: ILOAD_0(),
    0x1b: ILOAD_1(),
    0x1c: ILOAD_2(),
    0x1d: ILOAD_3(),
    0x1e: LLOAD_0(),
    0x1f: LLOAD_1(),
    0x20: LLOAD_2(),
    0x21: LLOAD_3(),
    0x22: ILOAD_0(),  # FLOAD_0
    0x23: ILOAD_1(),  # FLOAD_1
    0x24: ILOAD_2(),  # FLOAD_2
    0x25: ILOAD_3(),  # FLOAD_3
    0x26: DLOAD_0(),
    0x27: DLOAD_1(),
    0x28: DLOAD_2(),
    0x29: DLOAD_3(),
    0x2a: ILOAD_0(),  # ALOAD_0
    0x2b: ILOAD_1(),  # ALOAD_1
    0x2c: ILOAD_2(),  # ALOAD_2
    0x2d: ILOAD_3(),  # ALOAD_3
    0x36: ISTORE(),
    0x37: LSTORE(),
    0x38: ISTORE(),  # FSTORE
    0x39: DSTORE(),
    0x3a: ISTORE(),  # ASTORE
    0x3b: ISTORE_0(),
    0x3c: ISTORE_1(),
    0x3d: ISTORE_2(),
    0x3e: ISTORE_3(),
    0x3f: LSTORE_0(),
    0x40: LSTORE_1(),
    0x41: LSTORE_2(),
    0x42: LSTORE_3(),
    0x43: ISTORE_0(),  # FSTORE_0
    0x44: ISTORE_1(),  # FSTORE_1
    0x45: ISTORE_2(),  # FSTORE_2
    0x46: ISTORE_3(),  # FSTORE_3
    0x47: DSTORE_0(),
    0x48: DSTORE_1(),
    0x49: DSTORE_2(),
    0x4a: DSTORE_3(),
    0x4b: ISTORE_0(),  # ASTORE_0
    0x4c: ISTORE_1(),  # ASTORE_1
    0x4d: ISTORE_2(),  # ASTORE_2
    0x4e: ISTORE_3(),  # ASTORE_3
    0x57: POP(),
    0x58: POP2(),
    0x59: DUP(),
    0x5a: DUP_X1(),
    0x5b: DUP_X2(),
    0x5c: DUP2(),
    0x5d: DUP2_X1(),
    0x5e: DUP2_X2(),
    0x5f: SWAP(),
    0x60: IADD(),
    0x61: LADD(),
    0x62: IADD(),  # FADD
    0x63: DADD(),
    0x64: ISUB(),
    0x65: LSUB(),
    0x66: ISUB(),  # FSUB
    0x67: DSUB(),
    0x68: IMUL(),
    0x69: LMUL(),
    0x6a: IMUL(),  # FMUL
    0x6b: DMUL(),
    0x6c: IDIV(),
    0x6d: LDIV(),
    0x6e: IDIV(),  # FDIV
    0x6f: DDIV(),
    0x70: IREM(),
    0x71: LREM(),
    0x72: IREM(),  # FREM
    0x73: DREM(),
    0x74: INEG(),
    0x75: LNEG(),
    0x76: INEG(),  # FNEG
    0x77: DNEG(),
    0x78: ISHL(),
    0x79: LSHL(),
    0x7a: ISHR(),
    0x7b: LSHR(),
    0x7c: IUSHR(),
    0x7d: LUSHR(),
    0x7e: IAND(),
    0x7f: LAND(),
    0x80: IOR(),
    0x81: LOR(),
    0x82: IXOR(),
    0x83: LXOR(),
    0x84: IINC(),
    0x85: I2L(),
    0x86: I2F(),
    0x87: I2D(),
    0x88: L2I(),
    0x89: L2F(),
    0x8a: L2D(),
    0x8b: F2I(),
    0x8c: F2L(),
    0x8d: F2D(),
    0x8e: D2I(),
    0x8f: D2L(),
    0x90: D2F(),
    0x91: I2B(),
    0x92: I2C(),
    0x93: I2S(),
    0x94: LCMP(),
    0x95: FCMPL(),
    0x96: FCMPG(),
    0x97: DCMPL(),
    0x98: DCMPG(),
    0x99: IFEQ(),
    0x9a: IFNE(),
    0x9b: IFLT(),
    0x9c: IFGE(),
    0x9d: IFGT(),
    0x9e: IFLE(),
    0x9f: IF_ICMPEQ(),
    0xa0: IF_ICMPNE(),
    0xa1: IF_ICMPLT(),
    0xa2: IF_ICMPGE(),
    0xa3: IF_ICMPGT(),
    0xa4: IF_ICMPLE(),
    0xa5: IF_ACMPEQ(),
    0xa6: IF_ACMPNE(),
    0xa7: GOTO(),
    0xaa: TABLE_SWITCH(),
    0xab: LOOKUP_SWITCH(),
    0xac: IRETURN(),
    0xad: LRETURN(),
    0xae: IRETURN(),  # FRETURN
    0xaf: DRETURN(),
    0xb0: IRETURN(),  # ARETURN
    0xb1: RETURN(),
    0xb2: GET_STATIC(),
    0xb3: PUT_STATIC(),
    0xb4: GET_FIELD(),
    0xb5: PUT_FIELD(),
    0xb6: INVOKE_VIRTUAL(),
    0xb7: INVOKE_SPECIAL(),
    0xb8: INVOKE_STATIC(),
    0xb9: INVOKE_INTERFACE(),

    0xbb: NEW(),
    0xc0: CHECK_CAST(),
    0xc1: INSTANCE_OF(),

    0xc4: WIDE(),
    0xc6: IFNULL(),
    0xc7: IFNONNULL(),
    0xc8: GOTO_W(),
}
