from Formula import syntaxType

class VariableTable:
    table = dict()
    def __init__(self) -> None:
        pass
    def Push(self,name,x):
        if(name in self.table):
            print('ERROR: 变量已经存在!')
            return 
        self.table[name] = x
    def Update(self,name,x):
        if(name in self.table):
            self.table[name] = x
            return 
        print('ERROR: 赋值失败,变量不存在!')
    def Get(self,name):
        if(name in self.table):
            return self.table[name]
        raise SystemError('ERROR: 变量不存在!')
        return None
    def DirctPush(self,name,x):
        self.table[name] = x
  
class ExecuteAbstractSyntax:
    syntaxtree = None
    variabletable = VariableTable()
    def __init__(self):
        pass

    def biasParse(self,node):
        if(node == None):
            return 0
        if(node.type == syntaxType.NUMBER):
            return int(node.token.get_contxt())
        elif(node.type == syntaxType.IDENTIFIER):
            return int(self.variabletable.Get(node.token.get_contxt()))
        elif(node.type == syntaxType.PAREN):
            return self.expressionParse(node.right)
    def multipParse(self,node): # 罗辑: 孩子们,我们要进画里了\
        if(node.type == syntaxType.NUMBER or node.type == syntaxType.IDENTIFIER):
            return self.biasParse(node)
        
        left = self.biasParse(node.left)
        if(node.right == None):
            return left
        right = self.biasParse(node.right)
        right_type = node.right.type 
        if(right_type == syntaxType.NUMBER or right_type == syntaxType.PAREN or right_type == syntaxType.IDENTIFIER):
            right = self.biasParse(node.right)
        else:
            # if(right_type == syntaxType.MUL or right_type == syntaxType.ADD)
            right = self.expressionParse(node.right)
        if(node.type == syntaxType.MUL):
            return self.operate('*',left,right)
        return 1
    def operate(self,op,left,right):
        # 无限大な梦のあとの 何もない世の中じゃ如
        # left = int(left.get_contxt())
        # right = int(right.get_contxt())
        if(op == '+' ):
            return left+right
        elif(op == '-'):
            return left - right
        elif(op== '*'):
            return left * right
        elif(op == '/'):
            return left / right
        elif(op == '&'):
            if(left > 0 and right >  0):
                return 1
            else:
                return 0
        elif(op == '|') :
            if(right > 0 or left > 0):
                return 1
            else:
                return 0       
        elif(op == '>'):
            if(left > right):
                return 1 
            else:
                return 0
        elif(op == '<') :
            if(left < right):
                return 1 
            else:
                return 0
        elif(op == '>='):
            if(left >= right):
                return 1 
            else:
                return 0
        elif(op == '<=') :
            if(left <= right):
                return 1 
            else:
                return 0
    def additveParse(self,node):
        op = None
        if(node.type == syntaxType.ADD):
            op = node.token.get_contxt()
            left = self.expressionParse(node.left)
            right = self.expressionParse(node.right)
        return self.operate(op,left,right)
    def logicParse(self,node):
        left = self.expressionParse(node.left)
        right = self.expressionParse(node.right)
        return self.operate(node.token.get_contxt(),left,right)
    def relationParse(self,node):
        left = self.expressionParse(node.left)
        right = self.expressionParse(node.right)
        return self.operate(node.token.get_contxt(),left,right)

    def expressionParse(self,node):
        if(node.type == syntaxType.ADD):
            return self.additveParse(node)
        elif(node.type == syntaxType.MUL):
            return self.multipParse(node)
        elif(node.type == syntaxType.LOGIC):
            return self.logicParse(node)
        elif(node.type == syntaxType.NUMBER):
            return int(node.token.get_contxt())
        elif(node.type == syntaxType.IDENTIFIER):
            return self.biasParse(node)
        elif(node.type == syntaxType.RELATIONALOPERATION):
            return self.relationParse(node)
        return 0
    def execute(self,syntaxtree):
        # if(syntaxtree.type == syntaxType.NUMBER):
        #     print(syntaxtree.token.get_contxt())
        # if(syntaxtree.type == syntaxType.IDENTIFIER):
        #     if(syntaxtree.left == None and syntaxtree.right==None):
        #         output = self.variabletable.Get(syntaxtree.token.get_contxt())
        #         if(output != None):
        #             print(output)
        #     else:
        #         print
        # 私は神です、コードの世界で現実逃避したいのです
        if(syntaxtree.left == None and syntaxtree.right ==None):
            if(syntaxtree.type == syntaxType.IDENTIFIER):
                print(self.variabletable.Get(syntaxtree.token.get_contxt()))
            elif(syntaxtree.type == syntaxType.NUMBER):
                print(int(syntaxtree.token.get_contxt()))
        else:
            if(syntaxtree.type == syntaxType.IDENTIFIER):
              if(syntaxtree.left.type == syntaxType.ASSIGNMENT):
                    self.variabletable.DirctPush(syntaxtree.token.get_contxt(),self.expressionParse(syntaxtree.left.left))      
            else:
                print(self.expressionParse(syntaxtree))        
                              
                  
                  
                

            


            

