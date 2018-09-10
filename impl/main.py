

if __name__ == "__main__":

    #read parameters from file-tag
    from impl.posReader import PosFile
    from impl.memmapping import CmppDriver, Movimentador_Generico
    driver = CmppDriver("CMPP00LG", funcionality=Movimentador_Generico)
    pos = PosFile('../pos/standard.toml', driver)
    paramBundle = pos.readTag('referenciar_z')

    posicaoFinal = driver.makeParam(key=driver.functionality.Posicao_final)
    posicaoFinal.value = 200

    paramBundle.update(posicaoFinal)

    from impl.communication import CmppAvenue, sendParamsToCmpp
    # configure port/channel
    avenue = CmppAvenue(channel=3, port='COM1')
    # send parameters to PCI-CMPP
    err, paramBundle = avenue.transact(paramBundle)

