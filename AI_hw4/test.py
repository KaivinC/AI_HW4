def CalGini(current,left,right):
    totalDC=0
    for i in current.values():
        totalDC+=i
    print(totalDC)
    Dc=1
    for i in current.values():
        Dc=Dc-(i/totalDC)*(i/totalDC)
    print(Dc)

current ={"a":2,"b":3,"c":4}
left ={"a":8,"b":7,"c":1}
right ={"a":5,"b":6,"c":0}
CalGini(current,left,right)