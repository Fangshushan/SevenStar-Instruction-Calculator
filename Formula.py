from  enum import Enum
LEFT = 1
RIGHT = 0
class syntaxType(Enum):
    ROOT = 1
    NUMBER = 2
    IDENTIFIER = 3
    INT = 4
    ASSIGNMENT = 5
    MUL = 6
    ADD = 7 
    PAREN = 8
    PARENEND = 9
    EXPRESSION = 10
    LOGICEXPRESSION = 11
    LOGIC = 12
    RELATIONALOPERATION = 13
class Node:
    left =None
    right = None
    def __init__(self,content,syntaxtype):
        self.token = content
        self.type = syntaxtype
    def Append_Branch(self,BT7274,token,syntaxtype,Direction):
        """
            return That add point father!
        """
        if(Direction == LEFT):
            if(BT7274.left == None):
                BT7274.left = Node(token,syntaxtype)
                return BT7274
            else:
                return self.Append_Branch(BT7274.left,token,syntaxtype,Direction)
        else:
            if(BT7274.right ==  None):
                BT7274.right = Node(token,syntaxtype)
                return BT7274
            else:
                return self.Append_Branch(BT7274.right,token,syntaxtype,Direction)
    def Dirct_AppendBranch(slef,BT7274,ENERGY,SELECT = LEFT):
        if(SELECT == LEFT):
            if(BT7274.left == None):
                BT7274.left = ENERGY
                return BT7274
            else:
                slef.Dirct_AppendBranch(BT7274.left,ENERGY,SELECT)
        else:
            if(BT7274.right == None):
                BT7274.right = ENERGY
                return BT7274
            else:
                slef.Dirct_AppendBranch(BT7274.right,ENERGY,SELECT)



    def MLR_Traversal(self,Nexus,Result,Dark=None,Direction=None,count = 0):
        """ The light will be passed down like a link  """
        if(Nexus == None):
            return Result
        if(Dark==None and Direction==None):
            Result += f'<[{self.token}]ROOT> --Type>>>>>>> {Nexus.type}\n'
        else:
            if Direction==LEFT:
                branchname = 'LEFT'    
            else:
                branchname = 'RIGHT'
            Result += ' '*(count+1) +'|'+ '='*(count)+'>> '+  f'<[{Nexus.token}] {branchname}> --Type--> {Nexus.type}\n'
        Result = self.MLR_Traversal(Nexus.left,Result=Result,Dark=Nexus,Direction=LEFT,count=count+1)
        Result = self.MLR_Traversal(Nexus.right,Result=Result,Dark=Nexus,Direction=RIGHT,count=count+1)
        return Result
    def __str__(self):
        return self.MLR_Traversal(Nexus=self,Result='',Dark=None,Direction=None,count=0)
class TokenReader:
    __readlocation = 0
    def __init__(self,tokenState,tokenList):
        self.tokenState = tokenState
        self.tokenList = tokenList
        self.tokenLen = len(tokenList)
    def forward(self):
        if(self.__readlocation + 1 > self.tokenLen):
            return None
        if( self.tokenList[self.__readlocation + 1].get_type() == self.tokenState.END):
            return None
        self.__readlocation +=1
        return self.tokenList[self.__readlocation]
    def peek(self):
        if(self.__readlocation + 1 <= self.tokenLen - 1):
            return self.tokenList[self.__readlocation+1]
        return self.tokenList[self.tokenLen - 1]
    def read(self):
        return self.tokenList[self.__readlocation]
    def backward(self):
        if(self.__readlocation -1 < 0):
            return 0
        else:
            self.__readlocation  -= 1
            return self.tokenList[self.__readlocation]       
class AbstractSyntaxTree:
    token = None
    child = []
    tokenstate = None
    def __init__(self):
        self.hello = 1
    def baiscExpression(self):
        # 2
        token = self.token
        state = self.tokenstate
        tokenLoctype = lambda : token.read().get_type()
        if(tokenLoctype() == state.IntLiteral):
            bt7274 = token.read()
            return Node(bt7274,syntaxType.NUMBER)
        
        if(tokenLoctype() == state.Identifier):
            bt7274 = token.read()
            return Node(bt7274,syntaxType.IDENTIFIER)
        
        if(tokenLoctype() == state.Leftparenthesis):
            bt7274 = Node(token.read(),syntaxType.PAREN)
            token.forward()
            energy = self.Expression()
            if(energy != None):
                bt7274.Dirct_AppendBranch(bt7274,energy,RIGHT)
                if(token.forward() != None or token.peek().get_type() == state.END ):
                    if(token.read().get_type() == state.Rightparenthesis):
                           bt7274.Append_Branch(bt7274,token.read(),syntaxType.PARENEND,LEFT)
                           return bt7274
                    else:
                        raise SystemError('ERROR:左括号无右括号匹配!')
                else:
                    raise SystemError('ERROR:左括号需要一些表达式和右括号!')
            else:
                raise SystemError('ERROR: \'(\' 左括号旁无表达式输入!')
    
        return None
    
    def multiplicativeExpression(self):
        # 2 call this function  toeknNeed Step
        token = self.token
        state = self.tokenstate
        tokenLoctype = lambda :token.read().get_type()

        leftchild = self.baiscExpression()
        result = None


        if(leftchild != None):
            if(token.forward() != None):
                if(tokenLoctype() == self.tokenstate.MUL or tokenLoctype() == self.tokenstate.DIV):
                    result = Node(token.read(),syntaxType.MUL)
                    if(token.forward()!=None):
                        rightchild = self.multiplicativeExpression()
                        if(rightchild != None):
                            result.Dirct_AppendBranch(result,rightchild,RIGHT)
                            result.Dirct_AppendBranch(result,leftchild)
                        else:
                            raise SystemError('ERROR: 乘法表达式出现错误!')
                    else:
                        raise SystemError('ERROR: 乘法表达式出现错误!')
                else:
                    token.backward()
                    return leftchild
            else:
                return leftchild
        return result 

    def additiveExpression(self):
        # 2 
        token  =  self.token
        state = self.tokenstate
        tokenLoctype = lambda : token.read().get_type()
        leftchild = self.multiplicativeExpression()
        result = None
        # print("leftchild:",token.read())
        if(leftchild != None):
            if(token.forward()!=None):
                if(tokenLoctype() == state.ADD or tokenLoctype() == state.SUB):
                    result = Node(token.read(),syntaxType.ADD)
                    if(token.forward() != None):
                        rightchild = self.additiveExpression()
                        if(rightchild != None):
                            result.Dirct_AppendBranch(result,rightchild,RIGHT)
                            result.Dirct_AppendBranch(result,leftchild)
                        else:
                            raise SystemError('ERROR: 加法匹配失败!')
                    else:
                        raise SystemError(f'ERROR: 加法匹配失败!')
                else:
                   token.backward()
                   return leftchild
                
            else:
                return leftchild

        
        return result
    def Expression(self):
        # 2
        token = self.token
        state = self.tokenstate
        tokenLoctype = lambda : token.read().get_type()
        result = self.additiveExpression()
        newresult = None
        # temporary_storage = tokenLoctype()
        
        if(token.forward() != None):
            if(tokenLoctype() == state.AND or tokenLoctype() == state.OR):
                newresult = Node(token.read(),syntaxType.LOGIC)
                token.forward() # 自然选择前进四 <================================
                newresult.Dirct_AppendBranch(newresult,result,LEFT)
                rightchild = self.additiveExpression()
                if(rightchild != None):
                    newresult.Dirct_AppendBranch(newresult,rightchild,RIGHT)
                    return newresult
                else:
                    raise SystemError('ERROR:逻辑表达式左侧无匹配表达式,请输入!')
            else:
                token.backward()
        
            # elif(temporary_storage == state.Identifier): #后续优化
            #     if(token.read().get_type() == state.EQU):
            #         result.Append_Branch(result,token.read(),syntaxType.ASSIGNMENT,LEFT)
            #         token.forward()
            #         newresult = self.Expression()
            #         if(newresult == None):
            #             raise SystemError('ERROR: 变量无赋值内容')
            #         else:
            #             result.Dirct_AppendBranch(result,newresult,LEFT)

        return result

    def IntVariableExpression(self):
        # 1
        token  = self.token
        state = self.tokenstate
        tokenLoctype = lambda : token.read().get_type()
        result = None

        if(tokenLoctype() == state.Int):
            result = Node(token.read(),syntaxType.INT)
            if(token.forward().get_type() == state.Identifier):
                result.Append_Branch(result,token.read(),syntaxType.IDENTIFIER,LEFT)
                if(token.forward().get_type() == state.EQU):
                    result.Append_Branch(result,token.read(),syntaxType.ASSIGNMENT,LEFT)
                    if(token.forward()!=None):
                        equ_result = self.RelationalExpression() # 1
                        if(equ_result != None): 
                            result.Dirct_AppendBranch(result,equ_result,LEFT)
                        else:
                          raise SystemError('ERROR: 赋值语句( \'=\' )后无 赋值发生错误异常,请检查赋值')
                            
                    else:
                        raise SystemError('ERROR: 赋值语句( \'=\' )后无 赋值内容')
            else:
                raise SystemError(f'Error: INT 变量类型后出现非法字符{tokenLoctype()} ')
        return result
    def VariableExpression(self):
        token  = self.token
        state = self.tokenstate
        tokenLoctype = lambda : token.read().get_type()
        result = None
        if(tokenLoctype() == state.Identifier):
            result = Node(token.read(),syntaxType.IDENTIFIER)
            forward_tokentype = token.forward()
            if(forward_tokentype == None):
                return result
            if( forward_tokentype.get_type() == state.EQU):
                result.Append_Branch(result,forward_tokentype,syntaxType.ASSIGNMENT,LEFT)
                token.forward()
                expre = self.RelationalExpression()
                # print(token.read())
                if(expre != None):
                    result.Dirct_AppendBranch(result,expre,LEFT)
                else:
                    raise SystemError('ERROR: 赋值语句后非法.请重新赋值')
            else:
                token.backward()
                return None
        return result
    def RelationalExpression(self):
        token = self.token
        left =  self.Expression()
        peek = token.forward()
        state = self.tokenstate
        if(peek != None):
            peek = peek.get_type()
            if(peek == state.GT or peek == state.GE or peek == state.LT or peek == state.LE):
                result = Node(token.read(),syntaxType.RELATIONALOPERATION)
                
                if(token.forward() == None):
                    raise SystemError('ERROR: 关系表达式右侧并未赋值')
                right = self.Expression()
                if(right == None):
                    raise SystemError('ERROR: 关系表达式右侧错误赋值')
                else:
                    result.Dirct_AppendBranch(result,left,LEFT)
                    result.Dirct_AppendBranch(result,right,RIGHT)
                    return result
        else:
            return left
        return None



    def execute(self,tokenState,tokenList):
        self.token = TokenReader(tokenState,tokenList)
        self.tokenstate = tokenState
        child = self.IntVariableExpression()
        if(child == None):
            child = self.VariableExpression()
            if(child == None):
                child = self.RelationalExpression()
                if(child == None):
                    raise SystemError("ERROR:代码非法,暂时解析不了!") 
        self.child.append(child)

