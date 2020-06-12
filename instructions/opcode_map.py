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
    0x0A: LCONST_1(),
    0x0B: FCONST_0(),
    0x0C: FCONST_1(),
    0x0D: FCONST_2(),
    0x0E: DCONST_0(),
    0x0F: DCONST_1(),
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
    0x1A: ILOAD_0(),
    0x1B: ILOAD_1(),
    0x1C: ILOAD_2(),
    0x1D: ILOAD_3(),
    0x1E: LLOAD_0(),
    0x1F: LLOAD_1(),
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
    0x2A: ILOAD_0(),  # ALOAD_0
    0x2B: ILOAD_1(),  # ALOAD_1
    0x2C: ILOAD_2(),  # ALOAD_2
    0x2D: ILOAD_3(),  # ALOAD_3
    0x2E: IALOAD(),
    0x2F: LALOAD(),
    0x30: IALOAD(),  # FALOAD
    0x31: DALOAD(),
    0x32: IALOAD(),  # AALOAD
    0x33: IALOAD(),  # BALOAD
    0x34: CALOAD(),
    0x35: IALOAD(),  # SALOAD
    0x36: ISTORE(),
    0x37: LSTORE(),
    0x38: ISTORE(),  # FSTORE
    0x39: DSTORE(),
    0x3A: ISTORE(),  # ASTORE
    0x3B: ISTORE_0(),
    0x3C: ISTORE_1(),
    0x3D: ISTORE_2(),
    0x3E: ISTORE_3(),
    0x3F: LSTORE_0(),
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
    0x4A: DSTORE_3(),
    0x4B: ISTORE_0(),  # ASTORE_0
    0x4C: ISTORE_1(),  # ASTORE_1
    0x4D: ISTORE_2(),  # ASTORE_2
    0x4E: ISTORE_3(),  # ASTORE_3
    0x4F: IASTORE(),
    0x50: LASTORE(),
    0x51: IASTORE(),  # FASTORE
    0x52: DASTORE(),
    0x53: IASTORE(),  # AASTORE
    0x54: IASTORE(),  # BASTORE
    0x55: CASTORE(),
    0x56: IASTORE(),  # SASTORE
    0x57: POP(),
    0x58: POP2(),
    0x59: DUP(),
    0x5A: DUP_X1(),
    0x5B: DUP_X2(),
    0x5C: DUP2(),
    0x5D: DUP2_X1(),
    0x5E: DUP2_X2(),
    0x5F: SWAP(),
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
    0x6A: IMUL(),  # FMUL
    0x6B: DMUL(),
    0x6C: IDIV(),
    0x6D: LDIV(),
    0x6E: IDIV(),  # FDIV
    0x6F: DDIV(),
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
    0x7A: ISHR(),
    0x7B: LSHR(),
    0x7C: IUSHR(),
    0x7D: LUSHR(),
    0x7E: IAND(),
    0x7F: LAND(),
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
    0x8A: L2D(),
    0x8B: F2I(),
    0x8C: F2L(),
    0x8D: F2D(),
    0x8E: D2I(),
    0x8F: D2L(),
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
    0x9A: IFNE(),
    0x9B: IFLT(),
    0x9C: IFGE(),
    0x9D: IFGT(),
    0x9E: IFLE(),
    0x9F: IF_ICMPEQ(),
    0xA0: IF_ICMPNE(),
    0xA1: IF_ICMPLT(),
    0xA2: IF_ICMPGE(),
    0xA3: IF_ICMPGT(),
    0xA4: IF_ICMPLE(),
    0xA5: IF_ACMPEQ(),
    0xA6: IF_ACMPNE(),
    0xA7: GOTO(),
    0xAA: TABLE_SWITCH(),
    0xAB: LOOKUP_SWITCH(),
    0xAC: IRETURN(),
    0xAD: LRETURN(),
    0xAE: IRETURN(),  # FRETURN
    0xAF: DRETURN(),
    0xB0: IRETURN(),  # ARETURN
    0xB1: RETURN(),
    0xB2: GET_STATIC(),
    0xB3: PUT_STATIC(),
    0xB4: GET_FIELD(),
    0xB5: PUT_FIELD(),
    0xB6: INVOKE_VIRTUAL(),
    0xB7: INVOKE_SPECIAL(),
    0xB8: INVOKE_STATIC(),
    0xB9: INVOKE_INTERFACE(),
    0xBB: NEW(),
    0xBC: NEW_ARRAY(),
    0xBD: ANEW_ARRAY(),
    0xBE: ARRAY_LENGTH(),
    0xC0: CHECK_CAST(),
    0xC1: INSTANCE_OF(),
    0xC4: WIDE(),
    0xC5: MULTI_ANEW_ARRAY(),
    0xC6: IFNULL(),
    0xC7: IFNONNULL(),
    0xC8: GOTO_W(),
    0xFE: INVOKE_NATIVE(),
}
