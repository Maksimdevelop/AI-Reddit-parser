from config.config import config

def GetApi():
    if config.AI_PLATFORM == "gigachat":
        import AI.gigachat_api as gigachat_api
        api = gigachat_api.GigaChatAPI()

    return api