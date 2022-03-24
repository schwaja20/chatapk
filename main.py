import logging

while True:
    try:
        vstup = int(input('zadej cislo: '))
        c = "asdasd" * "asdasd"
    except TypeError:
        print("Operaci nelze provest")
    except ValueError:
        print("Nezadal jste cislo!")
    except Exception as e:                  #slo by to i bez toho exception, ale takhle to je lepsi :)
        print("Nastala chyba: ", e)
    else:
        print("Gratuluji, str -> int :)")

#try except se pouziva jen v kritickych castech kodu