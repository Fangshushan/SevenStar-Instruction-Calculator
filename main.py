import Token
import Formula
import Execute
if __name__ == '__main__':
    code_count = 0
    code = ''
    state  = Token.tokenState
    finite = Token.finiteAutomaton(state)
    formul = Formula.AbstractSyntaxTree()
    excute = Execute.ExecuteAbstractSyntax()
    print('StarCalc calculator ')
    print('    Version 0.01')
    while(1):
        code = input(' > ')
        if(len(code) == 0):
            continue
        finite.Input_Machine(code)
        formul.execute(Token.tokenState,finite.Get_receiverList())
        excute.execute(formul.child[code_count])
        code_count+=1
        if(code == 'exit()'): break
        if(code == 'relic'):
            print('We have a city to burn!')