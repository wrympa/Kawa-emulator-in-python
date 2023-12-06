import sys
import math 

variables = []
loadvars = []
varmap = {}
mapdepth = 0
recdepth = 0
fromif = False
ops = ['+', '-', '*', '/', '=', '!=', '>', '>=', '<', '<=', '=', '!=', 'and', 'or', 'zero?', 'null?', 'length', 'list?', 'car', 'cdr', 'cons', 'append', 'not', 'reverse', 'min', 'max', 'else', 'sqrt', 'expt', 'even?', 'odd?', 'quotient', 'remainder', 'negative?', 'positive?']
        
def mapfunction(currcommand):
    try:
        lis = []
        retlis = []
        brackbalance = 1
        op = '('
        indx = 1
        while brackbalance != 0:
            op += currcommand[indx]
            if currcommand[indx] == ')':
                brackbalance -= 1
            if currcommand[indx] == '(':
                brackbalance += 1
            indx += 1

        while indx < len(currcommand):
            if currcommand[indx] == ' ':
                indx += 1
            else:
                break

        if currcommand[indx] == "'":
            indx += 1
            curr = ''
            while indx < len(currcommand):
                if currcommand[indx] != ' ' and currcommand[indx] != ')' and currcommand[indx] != '(':
                    curr += currcommand[indx]
                elif curr != '':
                    lis.append(curr)
                    curr = ''
                indx += 1
        else:
            lisname = ''
            while indx < len(currcommand):
                if currcommand[indx] == ')':
                    break
                lisname += currcommand[indx]
                indx += 1
            lis = varmap[lisname]

        tempcheck = ''
        for i in range(1, 7):
            tempcheck += currcommand[i]

        level = mapdepth
        varname = 'mapval' + str(level)
        global mapdepth
        mapdepth += 1
        if tempcheck == 'lambda':
            indx = 9
            varname = ''
            while indx < len(currcommand):
                if currcommand[indx] == ')':
                    break
                varname += currcommand[indx]
                indx += 1
            
        for i in lis:
            varmap[varname] = i
            retlis.append(processcommand(op))
        mapdepth -= 1
        return retlis
    except:
        op = ''
        indx = 0
        while currcommand[indx] != ' ':
            op += currcommand[indx]
            indx += 1
        if op in varmap:
            op = varmap[op]
        lis = readlist(currcommand[indx:])
        minsize = len(lis[0])
        for i in range(1,len(lis)):
            minsize = min(minsize, len(lis[i]))
        retlis = []
        for i in range(minsize):
            val = 0
            if op == '-':
                val = 2*lis[0][0]
            if op == '*':
                val = 1
            if op == '/':
                val = lis[0][0] ** 2
            for j in lis:
                if op == '+':
                    try:
                        val += int(j[i])
                    except:
                        try:
                            val += float(j[i])
                        except:
                            return "ERROR: NOT INT"
                if op == '-':
                    try:
                        val -= int(j[i])
                    except:
                        try:
                            val -= float(j[i])
                        except:
                            return "ERROR: NOT INT"
                if op == '*':
                    try:
                        val *= int(j[i])
                    except:
                        try:
                            val *= float(j[i])
                        except:
                            return "ERROR: NOT INT"
                if op == '/':
                    try:
                        val /= int(j[i])
                    except:
                        try:
                            val /= float(j[i])
                        except:
                            return "ERROR: NOT INT"
            retlis.append(val)
        return retlis

def iffunction(currcommand):
    cond = '('
    brackbalance = 1
    indx = 1
    while brackbalance != 0:
        cond += currcommand[indx]
        if currcommand[indx] == ')':
            brackbalance -= 1
        if currcommand[indx] == '(':
            brackbalance += 1
        indx += 1

    indx += 1
    if currcommand[indx] == '(':
        res1 = '('
        brackbalance = 1
        indx += 1
        while brackbalance != 0:
            res1 += currcommand[indx]
            if currcommand[indx] == ')':
                brackbalance -= 1
            if currcommand[indx] == '(':
                brackbalance += 1
            indx += 1
    else:
        res1 = currcommand[indx]
        indx += 1
        while currcommand[indx] != ' ' and currcommand[indx] != ')':
            res1 += currcommand[indx]
            indx += 1
    indx += 1

    if currcommand[indx] == '(':
        res2 = '('
        brackbalance = 1
        indx += 1
        while brackbalance != 0:
            res2 += currcommand[indx]
            if currcommand[indx] == ')':
                brackbalance -= 1
            if currcommand[indx] == '(':
                brackbalance += 1
            indx += 1
    else:
        res2 = currcommand[indx]
        indx += 1
        while currcommand[indx] != ' ' and currcommand[indx] != ')':
            res2 += currcommand[indx]
            indx += 1
    global fromif       
    fromif = True
    res = processcommand(cond)
    fromif = False
    if res:
        if res1[0] == '(':
            return processcommand(res1)
        elif res1 in varmap:
            return varmap[res1]
        else:
            return res1
    else:
        if res2[0] == '(':
            return processcommand(res2)
        elif res2 in varmap:
            return varmap[res2]
        else:
            return res2

def lambdafunction(currcommand):
    variables = []
    currvar = ''
    op_start = 0
    howmanyvars = 0
    for i in range(1, len(currcommand)):
        if currcommand[i] == ' ' or currcommand[i] == ')':
            if currvar != '':
                variables.append(currvar)
                howmanyvars += 1
                currvar = ''
            if currcommand[i] == ')':
                op_start = i
                break
        else:
            currvar += currcommand[i]
    
    brackbal = 1
    while currcommand[op_start] != '(':
        op_start += 1
    
    val_start = 0
    op = '('
    brackbal = 1
    while brackbal != 0:
        op_start += 1
        val_start = op_start
        op += currcommand[op_start]
        if currcommand[op_start] == '(':
            brackbal += 1
        elif currcommand[op_start] == ')':
            brackbal -= 1

    while val_start < len(currcommand):
        if currcommand[val_start] == ' ' or currcommand[val_start] == '(' or currcommand[val_start] == ')':
            val_start += 1
        else:
            break

    varcounter = 0
    i = val_start
    while i < len(currcommand):
        currval = ''
        temp = i
        while temp < len(currcommand):
            if currcommand[temp] != ' ' and currcommand[temp] != '(' and currcommand[temp] != ')':
                currval += currcommand[temp]
                temp += 1
            else:
                break
        i = temp
        if currval != '' and varcounter < howmanyvars:
            varmap[variables[varcounter]] = currval
            varcounter += 1
        i += 1

    ret = processcommand(op)
    for i in variables:
        del varmap[i]
    return ret

def condfunction(currcommand):
    curcond = ''
    curexec = ''
    indx = 1
    while indx < len(currcommand):
        op = '('
        brackbalance = 1
        while brackbalance != 0:
            op += currcommand[indx]
            if currcommand[indx] == '(':
                brackbalance += 1
            if currcommand[indx] == ')':
                brackbalance -= 1
            indx += 1

        while indx < len(currcommand):
            if currcommand[indx] != '(':
                indx += 1
            else:
                break
        indx += 1

        newindx = 1
        if op[newindx] == '(':
            brackbalance = 1
            curcond = '('
            newindx += 1
            while brackbalance != 0:
                curcond += op[newindx]
                if op[newindx] == '(':
                    brackbalance += 1
                if op[newindx] == ')':
                    brackbalance -= 1
                newindx += 1
        else:
            curcond += op[newindx]
            newindx += 1
            while newindx < len(op):
                if op[newindx] == ' ' or op[newindx] == ')':
                    break
                else:
                    curcond += op[newindx]
                    newindx += 1
        
        while newindx < len(op):
            if op[newindx] == ' ':
                newindx += 1
            else:
                break

        if op[newindx] == '(':
            brackbalance = 1
            curexec = '('
            newindx += 1
            while brackbalance != 0:
                curexec += op[newindx]
                if op[newindx] == '(':
                    brackbalance += 1
                if op[newindx] == ')':
                    brackbalance -= 1
                newindx += 1
        else:
            curexec += op[newindx]
            newindx += 1
            while newindx < len(op):
                if op[newindx] == ' ' or op[newindx] == ')':
                    break
                else:
                    curexec += op[newindx]
                    newindx += 1
        global fromif
        fromif = True
        if processcommand(curcond):
            fromif = False
            return processcommand(curexec)
        global fromif
        fromif = False
        curcond = ''
        curexec = ''
    return 'all wrong'

def readlist(currcommand):
    retval = []
    brackbalance = 1
    indx = 1
    curname = ''
    while brackbalance != 0:
        if indx >= len(currcommand):
            break
        if currcommand[indx] == ' ' or currcommand[indx] == ')':
            if curname != '':
                if curname[0] == '(':
                    curname += ')'
                    curname = processcommand(curname)
                retval.append(curname)
                curname = ''
        elif currcommand[indx] == "'":
            curname = readlist(currcommand[(indx+1):])
            retval.append(curname)
            inner_brackbalance = 1
            indx += 2
            while inner_brackbalance != 0:
                if currcommand[indx] == '(':
                    inner_brackbalance += 1
                if currcommand[indx] == ')':
                    inner_brackbalance -= 1
                indx += 1
            curname = ''
        else:
            curname += currcommand[indx]
            if currcommand[indx] == '(':
                brackbalance += 1
                inner_brackbalance = 1
                indx += 1
                curname = '('
                while inner_brackbalance != 0:
                    curname += currcommand[indx]
                    if currcommand[indx] == '(':
                        inner_brackbalance += 1
                    if currcommand[indx] == ')':
                        inner_brackbalance -= 1
                    indx += 1
                curname = processcommand(curname)
                retval.append(curname)
                curname = ''
        if currcommand[indx] == ')':
            brackbalance -= 1
        indx += 1
    return retval

def opfunction(currcommand, cmp, lis):
    arglist = []
    curarg = ''
    indx = 0
    while indx < len(currcommand):
        if currcommand[indx] == ' ':
            indx += 1
        else:
            break
    if len(lis) == 0:
        arglist = readlist(' '+currcommand)
    else:
        arglist = lis
    print(arglist)
    tempnames = []
    for i in range(len(arglist)):
        try:
            if arglist[i] in varmap:
                tempnames.append(arglist[i])
                arglist[i] = varmap[arglist[i]]
            else:
                tempnames.append('')
        except:
            indx += 1
            indx -=1
            tempnames.append('')
       
    if cmp != 'length' and cmp != 'null?' and cmp != 'list?' and cmp != 'car' and cmp != 'cdr' and cmp != 'cons' and cmp != 'append' and cmp != 'and' and cmp != 'or' and cmp != 'min' and cmp != 'max' and cmp != 'reverse':
        for i in range(len(arglist)):
            arglist[i] = str(arglist[i])

    if cmp == '+':
        retval = 0
        for i in arglist:
            try:
                retval += int(i)
            except:
                try:
                    retval += float(i)
                except:
                    return 'ERROR: NOT NUM'
        if len(arglist) < 2:
            return 'ERROR: MORE THAN ONE NUM NEEDED'
        return retval
    elif cmp == '-':
        try:
            retval = int(arglist[0])
        except:
            try:
                retval = float(arglist[0])
            except:
                return 'ERROR: NOT NUM'
        for i in range(1, len(arglist)):
            try:
                retval -= int(arglist[i])
            except:
                try:
                    retval -= float(arglist[i])
                except:
                    return 'ERROR: NOT NUM'
        if len(arglist) < 2:
            return 'ERROR: MORE THAN ONE NUM NEEDED'
        return retval
    if cmp == '*':
        retval = 1
        for i in arglist:
            try:
                retval *= int(i)
            except:
                try:
                    retval *= float(i)
                except:
                    return 'ERROR: NOT NUM'
        if len(arglist) < 2:
            return 'ERROR: MORE THAN ONE NUM NEEDED'
        return retval
    if cmp == '/':
        try:
            retval = float(arglist[0]) 
        except:
            return 'ERROR: NOT NUM'
        for i in range(1, len(arglist)):
            try:
                retval /= int(arglist[i])
            except:
                try:
                    retval /= float(arglist[i])
                except:
                    return 'ERROR: NOT NUM'
        if len(arglist) < 2:
            return 'ERROR: MORE THAN ONE NUM NEEDED'
        return retval
    elif cmp == '=':
        retval = True
        for i in range(len(arglist)-1):
            if arglist[i] != arglist[i+1]:
                retval = False
        return retval
    elif cmp == '!=':
        retval = True
        for i in range(len(arglist)-1):
            if arglist[i] == arglist[i+1]:
                retval = False
        return retval
    elif cmp == '>':
        retval = True
        for i in range(1, len(arglist)):
            if arglist[0] <= arglist[i]:
                retval = False
        return retval
    elif cmp == '>=':
        retval = True
        for i in range(1, len(arglist)):
            if arglist[0] < arglist[i]:
                retval = False
        return retval
    elif cmp == '<':
        retval = True
        for i in range(1, len(arglist)):
            if arglist[0] >= arglist[i]:
                retval = False
        return retval
    elif cmp == '<=':
        retval = True
        for i in range(1, len(arglist)):
            if arglist[0] > arglist[i]:
                retval = False
        return retval
    elif cmp == 'and':
        for i in range(len(arglist)):
            if not arglist[i]:
                return False
        return True
    elif cmp == 'or':
        for i in range(len(arglist)):
            if arglist[i]:
                return True
        return False
    elif cmp == 'zero?':
        curarg = arglist[0]
        try:
            if curarg in varmap:
                if int(varmap[curarg]) == 0:
                    return True
                else:
                    return False
            else:
                if int(curarg) == 0:
                    return True
                else:
                    return False
        except:
            if curarg in varmap:
                if float(varmap[curarg]) == 0:
                    return True
                else:
                    return False
            else:
                if float(curarg) == 0:
                    return True
                else:
                    return False
    elif cmp == 'null?':
        curarg = arglist[0]
        if len(curarg) == 0:
            return True
        else:
            return False
    elif cmp == 'length':
        curarg = arglist[0]
        return len(curarg)
    elif cmp == 'list?':
        curarg = arglist[0]
        if isinstance(curarg, list):
            return True
        else:
            return False
    elif cmp == 'car':
        curarg = arglist[0]
        if isinstance(curarg, list):
            try:
                return curarg[0]
            except:
                return 'List is empty'
        else:
            return 'ERROR: not list'
    elif cmp == 'cdr':
        curarg = arglist[0]
        if isinstance(curarg, list):
            try:
                retval = []
                for i in range(1, len(curarg)):
                    if isinstance(curarg[i], list):
                        retval += [curarg[i]]
                    else:
                        retval += curarg[i]
                global fromif
                if not fromif:
                    varmap[tempnames[0]] = retval
                return retval
            except:
                return 'ERROR: list empty'
        else:
            return 'ERROR: not list'
    elif cmp == 'cons':
        curarg = arglist[1]
        if isinstance(curarg, list):
            curarg.insert(0, arglist[0])
            return curarg
        else:
            return "ERROR: NOT LIST"
    elif cmp == 'append':
        try:
            retval = []
            for i in arglist:
                retval += i
            return retval
        except:
            return 'ERROR: not list'
    elif cmp == 'max':
        try:
            arglist.sort()
            return arglist[len(arglist)-1]
        except:
            return 'ERROR: not list'
    elif cmp == 'min':
        try:
            arglist.sort()
            return arglist[0]
        except:
            return 'ERROR: not list'
    elif cmp == 'sqrt':
        try:
            a = arglist[0]
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            if a >= 0:
                return math.sqrt(a)
            else:
                return "ERROR: negative num"
        except:
            return 'ERROR: not num'
    elif cmp == 'expt':
        try:
            a = 0.0
            b = 0.0
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            if arglist[1] in varmap:
                a = varmap[arglist[1]]
            else:
                try:
                    a = int(arglist[1])
                except:
                    a = float(arglist[1])
            return a ** b
        except:
            return 'ERROR: not num'
    elif cmp == 'even?':
        try:
            a = 0.0
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            return a % 2 == 0
        except:
            return 'ERROR: not num'
    elif cmp == 'odd?':
        try:
            a = 0.0
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            return a % 2 == 1
        except:
            return 'ERROR: not num'
    elif cmp == 'quotient':
        try:
            a = 0.0
            b = 0.0
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            if arglist[1] in varmap:
                b = varmap[arglist[1]]
            else:
                try:
                    b = int(arglist[1])
                except:
                    b = float(arglist[1])
            return a / b
        except:
            return 'ERROR: not num'
    
    elif cmp == 'remainder':
        try:
            a = 0.0
            b = 0.0
            if arglist[0] in varmap:
                a = varmap[arglist[0]]
            else:
                try:
                    a = int(arglist[0])
                except:
                    a = float(arglist[0])
            if arglist[1] in varmap:
                b = varmap[arglist[1]]
            else:
                try:
                    b = int(arglist[1])
                except:
                    b = float(arglist[1])
            return a % b
        except:
            return 'ERROR: not num'
    elif cmp == 'positive?':
        curarg = arglist[0]
        try:
            if curarg in varmap:
                if int(varmap[curarg]) > 0:
                    return True
                else:
                    return False
            else:
                if int(curarg) > 0:
                    return True
                else:
                    return False
        except:
            if curarg in varmap:
                if float(varmap[curarg]) > 0:
                    return True
                else:
                    return False
            else:
                if float(curarg) > 0:
                    return True
                else:
                    return False
    elif cmp == 'negative?':
        curarg = arglist[0]
        try:
            if curarg in varmap:
                if int(varmap[curarg]) < 0:
                    return True
                else:
                    return False
            else:
                if int(curarg) < 0:
                    return True
                else:
                    return False
        except:
            if curarg in varmap:
                if float(varmap[curarg]) < 0:
                    return True
                else:
                    return False
            else:
                if float(curarg) < 0:
                    return True
                else:
                    return False
    elif cmp == 'reverse':
        try:
            temp = arglist[0]
            temp.reverse()
            return temp
        except:
            return 'ERROR: not list'
    elif cmp == 'not':
        try:
            temp = arglist[0]
            return not processcommand(temp)
        except:
            return 'ERROR: not expression'



def displayfunction(currcommand):
    if currcommand.rstrip(currcommand[-1]) in varmap:
        return varmap[currcommand.rstrip(currcommand[-1])]
    toprint = ''
    if currcommand[0] != '(':
        toprint = currcommand.rstrip(currcommand[-1])
    else:
        toprint = processcommand(currcommand[:-1])
    return toprint

def applyfunction(currcommand):
    op = ''
    indx = 0
    while currcommand[indx] != ' ':
        op += currcommand[indx]
        indx += 1
    vals = []
    indx += 1
    var = ''
    if currcommand[indx] == "'":
        indx += 2
        while indx < len(currcommand):
            if currcommand[indx] != '(':
                while currcommand[indx] != ' ' and currcommand[indx] != ')':
                    var += currcommand[indx]
                    indx += 1
                indx += 1
                if var != '':
                    vals.append(var)
                var = ''
            else:
                brackbalance = 1
                var = '('
                indx += 1
                while brackbalance != 0:
                    var += currcommand[indx]
                    if currcommand[indx] == '(':
                        brackbalance += 1
                    if currcommand[indx] == ')':
                        brackbalance -= 1
                    indx += 1
                indx += 1
                var = processcommand(var)
                if var != '':
                    vals.append(var)
                var = ''
    else:
        arg = '('
        brackbalance = 1
        indx += 1
        while brackbalance != 0:
            arg += currcommand[indx]
            if currcommand[indx] == '(':
                brackbalance += 1
            if currcommand[indx] == ')':
                brackbalance -= 1
            indx += 1
        vals = processcommand(arg)
    retval = 0
    if op == '+':
        for i in vals:
            try:
                retval += int(i)
            except:
                retval += float(i)
    elif op == '-':
        first = False
        for i in vals:
            if first:
                try:
                    retval -= int(i)
                except:
                    retval -= float(i)
            else:
                try:
                    retval += int(i)
                except:
                    retval += float(i)
                first = True
    elif op == '*':
        retval = 1
        for i in vals:
            try:
                retval *= int(i)
            except:
                retval *= float(i)
    elif op == '/':
        retval = 1
        first = False
        for i in vals:
            if first:
                try:
                    retval /= int(i)
                except:
                    retval /= float(i)
            else:
                try:
                    retval *= int(i)
                except:
                    retval *= float(i)
                first = True
    return retval

def valfunction(currcommand):
    name = ''
    value = ''
    indx = 1
    while indx < len(currcommand):
        if currcommand[indx] != ' ':
            name += currcommand[indx]
        else:
            break
        indx += 1
    indx += 1
    while indx < len(currcommand)-1:
        value += currcommand[indx]
        indx += 1
    if value[0] == '(':
        value = processcommand(value)
    varmap[name] = value

def letfunction(currcommand):
    brackbalance = 1
    indx = 1
    curvar = ''
    op = ''
    while brackbalance != 0 and indx < len(currcommand):
        if currcommand[indx] == '(':
            brackbalance += 1
        if currcommand[indx] == ')':
            brackbalance -= 1
        if currcommand[indx] == '(':
            brackbalance2 = 1
            curvar = "("
            indx += 1
            while brackbalance2 != 0:
                if currcommand[indx] == '(':
                    brackbalance2 += 1
                if currcommand[indx] == ')':
                    brackbalance2 -= 1
                curvar += currcommand[indx]
                indx += 1
            if indx < len(currcommand)-1:
                valfunction(curvar)
            else:
                op = curvar
            curvar = ''
        indx += 1
    return processcommand(op)

def fixstring(string):
    retval = ''
    temp = string.split(" ")
    while True:
        try:
            temp.remove('')
        except:
            break
    for i in range(len(temp)-1):
        if temp[i] != '':
            retval += temp[i]
            if temp[i][len(temp[i])-1] != '(' and temp[i+1][0] != ')':
                retval += ' '
    retval += temp[len(temp)-1]
    return retval

def loadfunction(currcommand):
    indx = 1
    filename = ''
    while currcommand[indx] != '"':
        filename += currcommand[indx]
        indx += 1
    file = open(filename, "r")

    strings = file.readlines()
    functs = []
    curstring = ''
    brackbalance = 0
    for i in strings:
        temp = i.replace('\n', '')
        indx = 0
        while indx < len(temp):
            curstring += temp[indx]
            if temp[indx] == '(':
                brackbalance += 1
            if temp[indx] == ')':
                brackbalance -= 1
            indx += 1
            if brackbalance == 0 and curstring != '':
                functs.append(curstring.strip())
                curstring = ''
    
    revamped = []
    for i in functs:
        x = i.strip()
        revamped.append(fixstring(x))
    for i in revamped:
        processcommand(i)

def definefunction(currcommand):
    indx = 0
    curname = ''
    functname = ''
    functvars = []

    if currcommand[indx] == '(':
        indx += 1
        while currcommand[indx] != ' ':
            functname += currcommand[indx]
            indx += 1

        while currcommand[indx] != ')':
            if currcommand[indx] == ' ':
                if curname != '':
                    functvars.append(curname)
                    curname = ''
                indx += 1
            curname += currcommand[indx]
            indx += 1
        if curname != '':
            functvars.append(curname)
    else:
        while currcommand[indx] != ' ':
            functname += currcommand[indx]
            indx += 1
        while indx < len(currcommand):
            if currcommand[indx] == ' ':
                indx += 1
            else:
                break
        val = ''
        while indx < len(currcommand)-1:
            val += currcommand[indx]
            indx += 1
        if val[0] == "'":
            val = readlist(val[1:])
        elif val[0] == '(':
            val = processcommand(val)
        varmap[functname] = val
        return

    if indx < len(currcommand) - 1:
        op = '('
        brackbalance = 1
        indx += 3
        while brackbalance != 0:
            op += currcommand[indx]
            if currcommand[indx] == '(':
                brackbalance += 1
            if currcommand[indx] == ')':
                brackbalance -= 1
            indx += 1
        varmap[functname] = [op, functvars]
    else:
        varmap[functname] = functvars[0]

def processcommand(currcommand):
    global fromif
    fromif = True
    if currcommand[0] == '(' and currcommand[1] == '(':
        return processcommand(currcommand[1:])
    operation = ''
    indx  = 0
    start = 0
    if currcommand[0] == '(':
        start = 1
    for i in range(start, len(currcommand)):
        if currcommand[i] == ' ' or  currcommand[i] == ')':
            indx = i 
            break
        operation += currcommand[i]
    if operation == 'lambda': return lambdafunction(currcommand[8:])
    elif operation == '+' : return opfunction(currcommand[3:], '+', [])
    elif operation == '-' : return opfunction(currcommand[3:], '-', [])
    elif operation == '*' : return opfunction(currcommand[3:], '*', [])
    elif operation == '/' : return opfunction(currcommand[3:], '/', [])
    elif operation == 'map' : return mapfunction(currcommand[5:])
    elif operation == 'if' : return iffunction(currcommand[4:])
    elif operation == 'cond' : return condfunction(currcommand[6:])
    elif operation == '=' : return opfunction(currcommand[3:], '=', [])
    elif operation == '!=' : return opfunction(currcommand[4:], '!=', [])
    elif operation == '>' : return opfunction(currcommand[3:], '>', [])
    elif operation == '>=' : return opfunction(currcommand[4:], '>=', [])
    elif operation == '<' : return opfunction(currcommand[3:], '<', [])
    elif operation == '<=' : return opfunction(currcommand[4:], '<=', [])
    elif operation == 'zero?' : return opfunction(currcommand[7:], 'zero?', [])
    elif operation == 'not' : return opfunction(currcommand[5:], 'not', [])
    elif operation == 'null?' : return opfunction(currcommand[7:], 'null?', [])
    elif operation == 'list?' : return opfunction(currcommand[7:], 'list?', [])
    elif operation == 'length' : return opfunction(currcommand[8:], 'length', [])
    elif operation == 'and' : return opfunction(currcommand[5:], 'and', [])
    elif operation == 'or' : return opfunction(currcommand[4:], 'or', [])
    elif operation == 'min' : return opfunction(currcommand[5:], 'min', [])
    elif operation == 'max' : return opfunction(currcommand[5:], 'max', [])
    elif operation == 'True' : return True
    elif operation == 'else' : return True
    elif operation == 'False' : return False
    elif operation == 'display' :
        print(displayfunction(currcommand[9:]))
        return ''
    elif operation == 'apply' : return applyfunction(currcommand[7:])
    elif operation == 'let' : return letfunction(currcommand[5:])
    elif operation == 'define' : definefunction(currcommand[8:])
    elif operation == 'car' : return opfunction(currcommand[5:], 'car', [])
    elif operation == 'cdr' : return opfunction(currcommand[5:], 'cdr', [])
    elif operation == 'cons' : return opfunction(currcommand[6:], 'cons', [])
    elif operation == 'append' : return opfunction(currcommand[8:], 'append', [])
    elif operation == 'reverse' : return opfunction(currcommand[9:], 'reverse', [])
    elif operation == 'sqrt' : return opfunction(currcommand[6:], 'sqrt', [])
    elif operation == 'expt' : return opfunction(currcommand[6:], 'expt', [])
    elif operation == 'even?' : return opfunction(currcommand[7:], 'even?', [])
    elif operation == 'odd?' : return opfunction(currcommand[6:], 'odd?', [])
    elif operation == 'quotient' : return opfunction(currcommand[10:], 'quotient', [])
    elif operation == 'remainder' : return opfunction(currcommand[11:], 'remainder', [])
    elif operation == 'negative?' : return opfunction(currcommand[10:], 'negative?', [])
    elif operation == 'positive?' : return opfunction(currcommand[11:], 'positive?', [])
    elif operation == 'eval' :
        arg = processcommand(currcommand[6:])
        return opfunction('', arg[0], arg[1:])
    elif operation == 'load' : return loadfunction(currcommand[6:])
    elif operation == 'list' : return readlist(currcommand[5:])
    elif operation in varmap :
        global ops
        if varmap[operation] in ops:
            return opfunction(currcommand[(len(operation)+2):], varmap[operation], [])
        try:
            global fromif
            fromif = False
            functvars = varmap[operation][1]
            curvars = []
            curvars = readlist(currcommand[indx:])
            level = recdepth
            global recdepth
            recdepth += 1
            temp = varmap[operation][0].split(' ')

            for i in range(len(temp)):
                if stripped(temp[i]) in functvars:
                    temp[i] = makeanew(temp[i], level)
            
            newstr = ''
            for i in temp:
                newstr += i +' '
            newstr.rstrip(newstr[-1])

            for i in range(len(functvars)):
                varmap[functvars[i] + str(level)] = curvars[i]
                varmap[functvars[i]] = curvars[i]
            retval = processcommand(newstr)
            recdepth -= 1
            return retval
        except:
            if varmap[operation][0] == '(':	
                return processcommand(varmap[operation])	
            else:	
                return varmap[operation]
    elif len(operation) > 0:
        if operation[0] == '"' : return operation

def makeanew(currcommad, level):
    retval = ''
    added = False
    for i in range(len(currcommad)):
        if currcommad[i] == ')' and (not added):
            retval += str(level)
            retval += ')'
            added = True
        else:
            retval += currcommad[i]
    return retval

def stripped(currcommand):
    retval = ''
    for i in range(len(currcommand)):
        if currcommand[i] != ')' and currcommand[i] != '(':
            retval += currcommand[i]
    
    return retval

def main():
    global varmap
    startword = ''
    startword = sys.stdin.readline()
    startword = startword.rstrip(startword[-1])
    while True :
        if startword == 'kawa' :
            break
        startword = sys.stdin.readline()
        startword = startword.rstrip(startword[-1])
    currcommand = ''
    ordernum = 1
    while currcommand != '(exit())':
        sys.stdout.write('#|kawa:'+str(ordernum)+'|# ')
        currcommand = sys.stdin.readline()
        currcommand = currcommand.rstrip(currcommand[-1])
        currcommand = currcommand.strip()
        currcommand = fixstring(currcommand)
        toprint = processcommand(currcommand)
        if toprint != '' and toprint != None:
            print(toprint)
        variables = []
        ordernum+=1



if __name__ == "__main__":
  main()