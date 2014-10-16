def kilocalc(vol):
    percentvol = vol/100.0
    kilo = (percentvol * 1000.0)

    return kilo


def main():
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
        result = kilocalc(recipe.get(i))
        print i, "=", result, "grams"




if __name__ == "__main__":
    main()
 