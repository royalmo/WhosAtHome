import telepot



class BotHandler:
    def __init__(self, bot : telepot.Bot, repo_path : str) -> None:
        self.bot = bot
        self.repo_path = repo_path

    def new_message(self, ctx : dict) -> None:

        # Getting message info
        content_type, chat_type, chat_id = telepot.glance(ctx)
        user_id = ctx["from"]["id"]
        language = ctx["from"]["language_code"]
        print(language)

        # Accepting only text messages
        if content_type != "text":
            print("Error")
            return