def kiloCalc(vol):
    percentvol = vol/100.0
    kilo = (percentvol * 1000.0)

    return kilo

def purpleGlaze():
    print "Purple Glaze Recipe"
    recipe = {
        "pf" : 29.3,
        "sil" : 24.1,
        "wh" : 9.0,
        "kao" : 6.8,
        "dol" : 6.8,
        "talc" : 13.5,
        "gbor" : 10.5,
        "zirc" : 8.0,
        "color" : 1.0,
        }

    for i in recipe:
        result = kiloCalc(recipe.get(i))
        print i, "=", result, "grams"

    return purpleGlaze


def howManyforBase():
    print "How many ingredients for base? "
    num = raw_input()

    return num

def getBaseClay(num):
    d = {}
    for i in range(num):
        print "Chem name: "
        chem = raw_input()
        print "Volume(percentage)"
        weight = raw_input()
        d[chem] = float(weight)
    return d

def getKilo(glazelist):
    kilos = {}
    weight = 0
    for i in glazelist:
        volume = glazelist.get(i)
        weight = kiloCalc(volume)
        kilos[i] = (weight)
    return kilos

def main():
    #purpleGlaze()

    x = howManyforBase()
    print "%s" % x
    xint = int (x)
    # print getBaseClay(xint)
    print getKilo(getBaseClay(xint))





if __name__ == "__main__":
    main()
