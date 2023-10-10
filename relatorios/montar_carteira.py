import bancoCentral

def main():
    selic=bancoCentral.SELIC(5)
    ipca=bancoCentral.IPCA(5)

    print(selic.media_anual())
    print(ipca.media_ganho_real())

if __name__ == "__main__":
    main()
