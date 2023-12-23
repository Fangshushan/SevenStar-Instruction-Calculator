from enum import Enum

class tokenState(Enum):
    END = -2 
    ACCEPT = -1
    INIT = 0 # init
    GT = 1 # >
    GE = 2 # >=
    Identifier = 3 # var_name
    IntLiteral = 4 # con_value
    MUL = 5 # *
    ADD = 6 # +
    DIV = 7 # /
    SUB = 8 # - 
    EQU = 9 #==
    LT = 10 # < 
    LE = 11 # <=
    Int = 12 # int
    Float = 13 # flot 
    Bool = 14 # 
    BLANK = 15
    Leftparenthesis = 16
    Rightparenthesis = 17
    AND = 18
    OR = 19
    NOT  = 20

class Token:
    def __init__(self,context,state_type):
        self.context = context
        self.type = state_type
    def get_type(self):
        return self.type
    def get_contxt(self):
        return self.context
    def __call__(self,contxt,state_type):
        self.context = contxt
        self.type = state_type
    def __str__(self):
        return f"tokenType:{self.type} tokenContxt:{self.context}"

class finiteAutomaton:
    def __init__(self,state):
        self.state = state
        self.receiverList = []
    def Initial_State(self,ch):
        if(ch.isalpha()):
            return self.state.Identifier
        elif(ch.isdigit()):
            return self.state.IntLiteral
        elif(ch == '>'):
            return self.state.GT
        elif(ch == '+'):
            return self.state.ADD
        elif(ch == '-'):
            return self.state.SUB
        elif(ch == '*'):
            return  self.state.MUL
        elif(ch == '/'):
            return self.state.DIV
        elif(ch == '='):
            return  self.state.EQU  
        elif(ch == '<'):
            return self.state.LT            
        elif(ch == ' ' or ch == '\t' or ch == '\n'):
            return self.state.BLANK
        elif(ch == '$'):
            return self.state.END
        elif(ch == '('):
            return self.state.Leftparenthesis
        elif(ch == ')'):
            return self.state.Rightparenthesis
        elif(ch == '&'):
            return self.state.AND
        elif(ch == '|'):
            return self.state.OR
        elif(ch == '!'):
            return self.state.NOT
        else:
            raise EOFError(f'包含非法符号{ch}')
    def State_Transition(self,previousState,ch):
        # ch in Advance , if ch is state, eat else set now
        ACCEPT = self.state.ACCEPT
        BLANK = self.state.BLANK
        END = self.state.END
        if(previousState == self.state.Identifier):
            if(ch.isalpha() or ch.isdigit()):
                return self.state.Identifier
            else:
                return ACCEPT
        elif (previousState == self.state.GT):
            if(ch == '='):
                return self.state.GE
            else:
                return ACCEPT
        elif (previousState == self.state.IntLiteral):
            if(ch.isdigit()):
                return self.state.IntLiteral
            else:
                return ACCEPT
        elif(previousState == self.state.LT):
            if(ch == '='):
                return self.state.LE
            else:
                return ACCEPT
        elif (previousState == self.state.GE):
            return ACCEPT
        elif (previousState == self.state.ADD):
            return ACCEPT
        elif (previousState == self.state.SUB):
            return ACCEPT
        elif (previousState == self.state.MUL):
            return ACCEPT
        elif (previousState == self.state.DIV):
            return ACCEPT
        elif (previousState == self.state.EQU):
            return ACCEPT
        elif(previousState == self.state.LE):
            return ACCEPT
        elif(previousState == self.state.Leftparenthesis):
            return ACCEPT
        elif(previousState == self.state.Rightparenthesis):
            return ACCEPT
        elif(previousState == self.state.AND):
            return ACCEPT
        elif(previousState == self.state.OR):
            return ACCEPT
        elif(previousState == self.state.NOT):
            return ACCEPT
        elif(previousState == BLANK):
            if ch ==' ' or ch =='\t':
                return BLANK
            else:
                return ACCEPT
        elif(previousState == END):
            # print('!!!')
            if(ch=='$'):
                #   print('!!!')
                  return ACCEPT
            else:
                raise Exception('here $ is error!')
    def Get_receiverList(self):
        result = self.receiverList
        self.receiverList = []
        return result
    def peep(self,line,loc,len):
        if(loc+1 > len+1):
            return line[len]
        return line[loc+1]
    
    def Input_Machine(self,line):
        peek = lambda x :self.peep(line+'$$',x,len(line))
        line+='$$'
        INIT = self.state.INIT
        BLANK = self.state.BLANK
        END = self.state.END
        ACCEPT = self.state.ACCEPT
        preState = INIT 
        nState = INIT
        chReceive = ''
        initchReceive = False

        # BLANK AND END QUESTION 
        for loc in range(0,len(line)):
            pre_ch = peek(loc)  # 偷看一下
            ch = line[loc] # 当前
            if nState == INIT:
                nState = self.Initial_State(ch)
                # if nState!= BLANK:
                #     chReceive+=ch
                #     initchReceive = True
            preState = nState # 上个字符 
            nState = self.State_Transition(preState,pre_ch)
            if nState!= BLANK and preState != BLANK:
                chReceive+=ch
            if(nState == ACCEPT):
                if(preState==BLANK): # NEXT is't BLANK
                    nState = INIT
                    loc+=1
                    continue
                elif preState==END:
                    if(loc < len(line)-2):
                        raise ConnectionError('语句中包含错误的退出符号')
                    self.receiverList.append(Token('END',END))
                    return ACCEPT # AC ^ v ^
                if(preState == tokenState.Identifier):
                    if chReceive == 'int':
                        preState = tokenState.Int
                    elif chReceive == 'float':
                        preState = tokenState.Float

                self.receiverList.append(Token(chReceive,preState))
                chReceive =''
                nState = INIT
            # initchReceive = True