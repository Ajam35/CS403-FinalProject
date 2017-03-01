#python finaleproject.py to compile in terminal.


class circuit(object):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2

class andgate(circuit):

    def cir_func(self):
        return self.in1_ and self.in2_

class andgate_3in(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def cir_func(self):
        return self.in1_ and self.in2_ and self.in3_

class andgate_5in(circuit):
    def __init__(self, in1, in2, in3, in4, in5):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5

    def cir_func(self):
        return self.in1_ and self.in2_ and self.in3_ and self.in4_ and self.in5_

class andgate_6in(circuit):
    def __init__(self, in1, in2, in3, in4, in5, in6):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5
        self.in6_ = in6

    def cir_func(self):
        return self.in1_ and self.in2_ and self.in3_ and self.in4_ and self.in5_ and self.in6_

class orgate(circuit):
    def cir_func(self):
        return self.in1_ or self.in2_

class orgate_3in(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def cir_func(self):
        return self.in1_ or self.in2_ or self.in3_

class orgate_4in(circuit):
    def __init__(self, in1, in2, in3, in4):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4

    def cir_func(self):
        return self.in1_ or self.in2_ or self.in3_ or self.in4_

class notgate(circuit):
    def __init__(self, in1):
        self.in1_ = in1

    def cir_func(self):
        return not self.in1_

class mux_2to1(circuit):
    def __init__(self, in1, in2, ctr1):
        self.in1_ = in1
        self.in2_ = in2
        self.ctr1_ = ctr1

    def cir_func(self):
        inv_ctr = notgate(self.ctr1_).cir_func()
        a0 = andgate(self.in1_, inv_ctr).cir_func()
        a1 = andgate(self.in2_, self.ctr1_).cir_func()
        o0 = orgate(a0, a1)

        return o0.cir_func()

class mux_4to1(circuit):
    def __init__(self, in1, in2, in3, in4, ctr0, ctr1):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.ctr1_ = ctr0
        self.ctr0_ = ctr1

    def cir_func(self):
        m0_output = mux_2to1(self.in1_, self.in2_, self.ctr0_).cir_func()
        m1_output = mux_2to1(self.in3_, self.in4_, self.ctr0_).cir_func()
        m3_output = mux_2to1(m0_output, m1_output, self.ctr1_).cir_func()

        return m3_output

class fulladder(circuit):
    def __init__(self, in1, in2, carryIn):
        self.in1_ = in1
        self.in2_ = in2
        self.carryIn_ = carryIn

    def cir_func(self):
        o_2andg_1_co = andgate(self.in1_, self.carryIn_).cir_func()
        o_2andg_2_co = andgate(self.in2_, self.carryIn_).cir_func()
        o_2andg_3_co = andgate(self.in1_, self.in2_).cir_func()

        carryOut = orgate_3in(o_2andg_1_co, o_2andg_2_co, o_2andg_3_co).cir_func()

        in1_inv = notgate(self.in1_).cir_func()
        in2_inv = notgate(self.in2_).cir_func()
        cin_inv = notgate(self.carryIn_).cir_func()

        o_3andg_1_sum = andgate_3in(in1_inv, in2_inv, self.carryIn_).cir_func()
        o_3andg_2_sum = andgate_3in(in1_inv, self.in2_, cin_inv).cir_func()
        o_3andg_3_sum = andgate_3in(self.in1_, self.in2_, self.carryIn_).cir_func()
        o_3andg_4_sum = andgate_3in(self.in1_, in2_inv, cin_inv).cir_func()

        sum = orgate_4in(o_3andg_1_sum, o_3andg_2_sum,o_3andg_3_sum, o_3andg_4_sum).cir_func()

        return sum, carryOut



class ALU_1bit(object):
    def __init__(self, in1, in2, cin, aluctrs):
        self.inp1 = in1
        self.inp2 = in2
        self.carrIn= cin
        self.aluCtr = aluctrs

    def cir_func(self):
        in1Inv = notgate(self.inp1).cir_func()
        in2Inv = notgate(self.inp2).cir_func()

        mux1 = mux_2to1(self.inp1, in1Inv, self.aluCtr[0]).cir_func()
        mux2 = mux_2to1(self.inp2, in2Inv, self.aluCtr[1]).cir_func()

        aluAnd = andgate(mux1, mux2).cir_func()
        aluOr = orgate(mux1, mux2).cir_func()
        sumOfAddr, carrOutAddr = fulladder(mux1, mux2, self.carrIn).cir_func()

        aluFalse = False

        aluRes = mux_4to1(aluAnd, aluOr, sumOfAddr, aluFalse, self.aluCtr[2], self.aluCtr[3]).cir_func()

        return aluRes, carrOutAddr

class ALU_32bit(object):
    def __init__(self, in1, in2, cin_bit0, aluctrs):
        self.inp1 = in1
        self.inp2 = in2
        self.cin_bit0_= cin_bit0
        self.aluctrs_ = aluctrs

    def cir_func(self):

        o_sum_32bitalu = [None]*32
        o_cout_32bitalu = [None]*32

        for i in range(31, -1, -1):

            if i == 31:
                cin = self.cin_bit0_
                o_sum_1bitalu, o_cout_1bitalu = ALU_1bit(self.inp1[i], self.inp2[i], cin, self.aluctrs_).cir_func()
            else:
                cin = o_cout_32bitalu[i+1]
                o_sum_1bitalu, o_cout_1bitalu = ALU_1bit(self.inp1[i], self.inp2[i], cin, self.aluctrs_).cir_func()

            o_sum_32bitalu[i] = o_sum_1bitalu
            o_cout_32bitalu[i] = o_cout_1bitalu

        return o_sum_32bitalu, o_cout_32bitalu[0]

class aluControl(circuit):
    def __init__(self, o1, o0, f5, f4, f3, f2, f1, f0):
        self.o1_ = o1
        self.o0_ = o0
        self.f5_ = f5
        self.f4_ = f4
        self.f3_ = f3
        self.f2_ = f2
        self.f1_ = f1
        self.f0_ = f0

    def cir_func(self):
        alu_ctrs = [None]*4

        ctr_0 = andgate(self.o0_, notgate(self.o0_).cir_func()).cir_func()

        ctr_1 = orgate(andgate(notgate(self.o1_).cir_func(), self.o0_).cir_func(), andgate(self.o1_, self.f1_).cir_func()).cir_func()

        ctr_2 = orgate(notgate(self.o1_).cir_func(), notgate(self.f2_).cir_func()).cir_func()

        ctr_3 = andgate(self.o1_, orgate(self.f3_, self.f0_).cir_func()).cir_func()

        alu_ctrs[0] = ctr_0
        alu_ctrs[1] = ctr_1
        alu_ctrs[2] = ctr_2
        alu_ctrs[3] = ctr_3
        return alu_ctrs

class registerFile(circuit):
    def __init__(self, reg_initial_value_b):
        self.registers = [None] * 32
        for reg in range(0, 32):
                self.registers[reg] = reg_initial_value_b

    def setRegValue(self, o_regDecoder, valueToSet):
        for i in range(0, 32):
            if o_regDecoder[i] ==True:
                self.registers[i] = valueToSet

    def getRegValue(self, o_regDecoder):
        for i in range(0, 32):
            if o_regDecoder[i] ==True:
                o_regValue = self.registers[i]
        return o_regValue

    def getAllRegValue(self):
        return self.registers

class decoderReg(circuit):
    def __init__(self, Instr_RegFiled):
        self.Instr_RegFiled_ = Instr_RegFiled

    def cir_func(self):
        o_decoderReg = [None]*32

        inv_Instr_RegFiled = [None]*5
        for i in range(0, 5):
            inv_Instr_RegFiled[i] = notgate(self.Instr_RegFiled_[i]).cir_func()

        o_decoderReg[0]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[1]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[2]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[3]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[4]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[5]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[6]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[7]  = andgate_5in(inv_Instr_RegFiled[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[8]  = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[9]  = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[10] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[11] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[12] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[13] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[14] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[15] = andgate_5in(inv_Instr_RegFiled[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[16] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[17] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[18] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[19] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[20] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[21] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[22] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[23] = andgate_5in(self.Instr_RegFiled_[0], inv_Instr_RegFiled[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[24] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[25] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[26] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[27] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], inv_Instr_RegFiled[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[28] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[29] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], inv_Instr_RegFiled[3], self.Instr_RegFiled_[4]).cir_func()
        o_decoderReg[30] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], inv_Instr_RegFiled[4]).cir_func()
        o_decoderReg[31] = andgate_5in(self.Instr_RegFiled_[0], self.Instr_RegFiled_[1], self.Instr_RegFiled_[2], self.Instr_RegFiled_[3], self.Instr_RegFiled_[4]).cir_func()

        return o_decoderReg

class mainCtrol(circuit):
    def __init__(self, op_5, op_4, op_3, op_2, op_1, op_0):
        self.op_5_ = op_5
        self.op_4_ = op_4
        self.op_3_ = op_3
        self.op_2_ = op_2
        self.op_1_ = op_1
        self.op_0_ = op_0

    def cir_func(self):
        o_6inand_0 = andgate_6in(notgate(self.op_5_).cir_func(), notgate(self.op_4_).cir_func(), notgate(self.op_3_).cir_func(), notgate(self.op_2_).cir_func(), notgate(self.op_1_).cir_func(), notgate(self.op_0_).cir_func()).cir_func()

        o_6inand_1 = andgate_6in(self.op_5_, notgate(self.op_4_).cir_func(), notgate(self.op_3_).cir_func(), notgate(self.op_2_).cir_func(), self.op_1_, self.op_0_).cir_func()
        o_6inand_2 = andgate_6in(self.op_5_, notgate(self.op_4_).cir_func(), self.op_3_, notgate(self.op_2_).cir_func(), self.op_1_, self.op_0_).cir_func()
        o_6inand_3 = andgate_6in(notgate(self.op_5_).cir_func(), notgate(self.op_4_).cir_func(), self.op_3_, notgate(self.op_2_).cir_func(), notgate(self.op_1_).cir_func(), notgate(self.op_0_).cir_func()).cir_func()

        o_RegDst = o_6inand_0
        o_AluSrc = orgate(o_6inand_1, o_6inand_2).cir_func()
        o_MemToReg = o_6inand_1
        o_RegWrite = orgate(o_6inand_0, o_6inand_1).cir_func()
        o_MemRead = o_6inand_1
        o_MemWrite = o_6inand_2
        o_Branch = o_6inand_3
        o_ALUOp1 = o_6inand_0
        o_ALUOp0 = o_6inand_3

        return o_RegDst, o_AluSrc, o_MemToReg, o_RegWrite, o_MemRead, o_MemWrite, o_Branch, o_ALUOp1, o_ALUOp0


class simpleMIPS(circuit):
    def __init__(self, instruction, registers):
        self.instru = instruction
        self.regis = registers
    
        
    def cir_func(self):

        ctrSig =[None]*4
        ctrSig[0] = False
        ctrSig[1] = False
        ctrSig[2] = True
        ctrSig[3] = False
        
        opCode = mainCtrol(self.instru[5], self.instru[4], self.instru[3], self.instru[2], self.instru[1], self.instru[0]).cir_func()
    
        aluContSig = aluControl(self.instru[7], opCode[8], self.instru[31], self.instru[30], self.instru[29], self.instru[28], self.instru[27], self.instru[26]).cir_func()

        if(aluContSig[0] == False and aluContSig[1] == True and aluContSig[2] == True and aluContSig[3] == False):
             cinbit = 1
        else:
             cinbit = 0
             
        rs = self.regis.getRegValue(decoderReg(self.instru[6:11]).cir_func())
     
        rt = self.regis.getRegValue(decoderReg(self.instru[11:16]).cir_func())

        rd = decoderReg(self.instru[16:21]).cir_func()

        alu32Call = ALU_32bit(rt, rs, cinbit ,aluContSig).cir_func()
                                                                         
        self.regis.setRegValue(rd,alu32Call[0]) 

       

def binaryToBoolean(input_binary, outputboolean):
    for i in range(0, len(input_binary)):
        one_or_zero = input_binary[i]
        if (one_or_zero == '1'):
            outputboolean[i] = True
        else:
            outputboolean[i] = False

def booleanToBinary_arr(input_boolean, outputbinary):
    for i in range(0, len(input_boolean)):
        TureOrFalse = input_boolean[i]
        if (TureOrFalse == True):
            outputbinary[i] = 1
        else:
            outputbinary[i] = 0

def main():


    '''
    final project:

    To get credit for the final project, you need to use the aluControl Class, ALU_32bit class, registerFile class, decoderReg class, and mainControl class.

    Following what we discussed in class, Implement a simpleMIPS object to fulfill the simulation of the R-format Instruction

    In your main function:

    1. Take a 32 bit instruction as the input:

        instru_b = [None]*32
        instru = raw_input("Please enter the complete instruction: ")
        binaryToBoolean(instru, instru_b)

    2. Initialize a register file with all registers with value 2(['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0'])

        reg_initial_value_b = [None]*32
        reg_initial_value = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0']
        binaryToBoolean(reg_initial_value, reg_initial_value_b)

        reg_file = registerFile(reg_initial_value_b)


    3. You need to use the simpleMIPS class, which implemented by yourself, to take the instruction instru_b and the register file reg_file, then excute the cir_func()
        simpleMIPSCPU = simpleMIPS(instru_b, reg_file)
        simpleMIPSCPU.cir_func()

    4.The register file reg_file should be updated depended the meaning of the input instruction:

        registers_values = reg_file.getAllRegValue()
        print "The registers value now are:"
        for i in range(0, len(registers_values)):
            print registers_values[i]

    e.g:

    the instruction 00000000110001110100011111100000

    means register 8 = register 6+ register 7

    after you executed the instruction, the register 8 should has value 4.

   Please enter the complete instruction: 00000000110001110100011111100000
The registers value now are:
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
[False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]

    '''

    instru_b = [None]*32
    instru = raw_input("Please enter the complete instruction: ")
    binaryToBoolean(instru, instru_b)

    reg_initial_value_b = [None]*32
    reg_initial_value = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0']
    binaryToBoolean(reg_initial_value, reg_initial_value_b)

    reg_file = registerFile(reg_initial_value_b)
    simpleMIPSCPU = simpleMIPS(instru_b, reg_file)
    simpleMIPSCPU.cir_func()

    registers_values = reg_file.getAllRegValue()
    print "The registers value now are:"
    for i in range(0, len(registers_values)):
        print registers_values[i]

if __name__ == '__main__':
    main()