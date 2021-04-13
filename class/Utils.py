import requests, json

class Utils():
    def __init__(self, Token):
        self.Token = Token
        self.BaseURI = "https://discord.com/api/v8"

    def Claim_Nitro(self, Code, ChanID):
        requests.post(f"{self.BaseURI}/entitlements/gift-codes/{Code}/redeem", headers= self.Header, data=json.dumps({ "channel_id": str(ChanID) }))

    def Token_Joiner(self, Invite):
        requests.post(f"{self.BaseURI}/invites/{Invite}", headers= { "Authorization": self.Token, "Content-Type": "application/json" })

    def Token_Send(self, ChanID, Message):
        requests.post(f"{self.BaseURI}/channels/{ChanID}/messages", headers= { "Authorization": self.Token, "Content-Type": "application/json" }, data=json.dumps({ "content": Message }))

    def Token_Friend_Request(self, UsrID):
        requests.put(f"{self.BaseURI}/users/@me/relationships/{UsrID}", headers= { "Authorization": self.Token, "Content-Type": "application/json" })
