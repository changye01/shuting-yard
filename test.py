# jump not Empty
a = [
    {'exp': [3]},
    {'exp': [1], "jump": ['JMP', 2]},
    {'exp': [1], 'jump': ['JNE', 3]},
    {'exp': [3]}
]

# for i in range(len(a)):
#     # print(a[i])
#     # print(a[i]['operator'][0])
#     if 'jump' in a[i] and len(a[i]['jump']):
#         print(a[i]['jump'])
#         jump = a[i]['jump']
#         if jump[0] == 'JNE':
#             print
#             i = jump[1]
#     print(i)


i = 0
while i < len(a):
    print(a[i])
    if 'jump' in a[i] and len(a[i]['jump']):
        jump = a[i]['jump']
        exp = a[i]['exp']
        if jump[0] == 'JNE' and len(exp) and exp[0]:
            i = jump[1]
            continue
        elif jump[0] == 'JMP':
            i = jump[1]
            continue
    i = i+1