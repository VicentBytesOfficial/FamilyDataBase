def inputCheck(InputString: str, ErrorString: str, ListName: list[list[str]]):
    """Gets list of lists and iterates it searching if varName is in, 
    if it is then varName takes the list[1] value"""
    while True:
    # Pedimos el dato y lo pasamos a minúsculas en la misma línea
        VarName = input(f"{InputString}\n").lower()
        
        for list in ListName:
            if VarName in list:
                return list[1]

        print(f"{ErrorString}\n")