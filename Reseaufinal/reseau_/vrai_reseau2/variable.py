a = 1
stri=''
str_test = "Barrack,(9,8)"
to_mine = (0,)

def transform_string2(stri_var):#return tuple ("building name", position in tuple)
    position = (0,0)
    entity = ''

    string = stri_var.split(',')

    if len(string)>2:
        entity = string[0]
        print(f"the entity is {entity}")
        position = (int(string[1].translate({ord(i): None for i in '[]()'})),int(string[2].translate({ord(i): None for i in '[]()'})))
        str_test = ''
    return (entity,position)

def transform_string(stri_var):#return tuple ("building name", position in tuple)
    position = (0,0)
    entity = ''

    string = stri_var.split(',')

    if len(string)==3:
        entity = string[0]
        position = (int(string[1].translate({ord(i): None for i in '[]()'})),int(string[2].translate({ord(i): None for i in '[]()'})))
        str_test = ''
    if len(string)==5:
        entity = string[0]
        position = (int(string[1].translate({ord(i): None for i in '[]()'})),int(string[2].translate({ord(i): None for i in '[]()'})),int(string[3].translate({ord(i): None for i in '[]()'})),int(string[4].translate({ord(i): None for i in '[]()'})))
        if len(string) >= 0:
            entity = string[0]




    return (entity,position)




no_space=stri.replace(' ', '')

v2=no_space.translate({ord(i): None for i in '[]'}) # no [ and ]

v3=v2.split(",")
text= v3[0]
if len(v3)>1:
    pos_x= v3[1]
    print(pos_x)
if len(v3)>2:
    pos_y = v3[2]
    print(pos_y)


