class GuessAWord:
    word=""
    category=""
    missing=""
    hint=""
    channel_id=""
    channel_name=""
    def __init__(self,word,category,missing,hint):
        self.word=word
        self.category=category
        self.hint=hint
        self.missing=missing

    def guess(self,word):
        if word.lower()==self.word.lower():
            return True,""
         
        else:
            return False,""