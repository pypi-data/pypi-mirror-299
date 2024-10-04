from . import ndarrayT, frameT, listT, dictT, seriesT

def get_transformer(dataset, cols):
    print(type(dataset))
    name = type(dataset).__name__
    if name == "list":
        return listT.Transformer(dataset)
    elif name == "dict":
        return dictT.Transformer(dataset, cols)
    elif name == "ndarray":
        return ndarrayT.Transformer(dataset)
    elif name == "DataFrame":
        return frameT.Transformer(dataset, cols)
    elif name == "Series":
        return seriesT.Transformer(dataset)
    else:
        return None