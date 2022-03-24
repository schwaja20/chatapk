import logging

while True:
    try:
        vstup = int(input('zadej cislo: '))
    except TypeError:
        print("Operaci nelze provest")
    except ValueError:
        print("Nezadal jste cislo!")
    except Exception as e:                  #slo by to i bez toho exception, ale takhle to je lepsi :)
        print("Nastala chyba: ", e)
    else:
        print("Gratuluji, str -> int :)")

# try except se pouziva jen v kritickych castech kodu
# koukni se na www.realpython.com
# umrdej jeste ConnectionRefusedError
# finally se po projeti excepty pokusi zavrit kod

############ dodelej chatapk #################