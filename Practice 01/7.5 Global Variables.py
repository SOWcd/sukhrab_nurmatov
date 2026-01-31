#functions

a = 'Apple'

def Tim_Coock():
    print('Steve Jobs creator of', a)

Tim_Coock()


#Variables in-out function

A = 'Arcane'

def Riot_Games():
    A = 'property' #local Variable - property also operator
    print('Arcane is Riot Games', A)


Riot_Games()

print('I love', A)



#global Variable in Function

B = 'Portal'

def Valve():
    global B
    B = "Portal 2"
    print(B)

Valve()

print(B)


