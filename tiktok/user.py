class User:
    def __init__(self, **kwargs):
        self.follower_count: int = kwargs.get("follower_count")
        self.nickname: str = kwargs.get("nickname")
        self.signature: str = kwargs.get("signature")
        self.uid: str = kwargs.get("uid")
        self.unique_id: str = kwargs.get("unique_id")