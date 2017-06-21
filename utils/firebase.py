import requests
import json

from models.player import PlayerModel
from models.club import ClubModel
from models.token import TokenModel

class FireBase:
    server_id = "AAAA-NcShG0:APA91bHAXfuQHkZO7-XHpuzrEvyxuqQH7Hgktlnf-rJ2zP3t7ERh7bWE37jHLm8iQAIlxgEiF4iwxvLHVPpxXylbCdPslwap5slget0zJPSeXH2zAw70NvPUNwM32jf_mVnWG75Fkerx"
    header = {
        'Authorization': 'key={}'.format(server_id),
        'Content-Type': 'application/json'
    }
    push_url = "https://fcm.googleapis.com/fcm/send"

    @classmethod
    def send_push_notification(cls,data,receiver):
        payload = {
            "data": data,
            "to": receiver
        }
        res = requests.post(cls.push_url,
                            headers = cls.header,
                            data = json.dumps(payload))
        return res

    # send push notification for club chat
    @classmethod
    def send_club_chat_notification(cls,clubID):
        data = {
            "clubID": clubID,
            "title": "Club chat message",
            "content": "tap here to view"
        }
        payload = {
            "data": data,
            "to": "/topics/club_{}".format(clubID)
        }
        res = requests.post(cls.push_url,
                            headers = cls.header,
                            data = json.dumps(payload))
        if res.status_code == 200:
            return True
        else:
            print(res)
            return False

    # send push notification for tournament chat
    @classmethod
    def send_tournament_chat_notification(cls,clubID,tournamentID):
        data = {
            "clubID": clubID,
            "tournamentID": tournamentID,
            "title": "Tournament chat message",
            "content": "tap here to view"
        }
        payload = {
            "data": data,
            "to": "/topics/club_{}_tournament_{}".format(clubID,tournamentID)
        }
        res = requests.post(cls.push_url,
                            headers = cls.header,
                            data = json.dumps(payload))
        if res.status_code == 200:
            return True
        # else:
        print(res)
        return False

    # send push notification for private chat
    @classmethod
    def send_private_chat_notification(cls,senderID,receiverID):
        # first, check user token
        sender_token = TokenModel.find_token_by_player_id(senderID)
        receiver_token = TokenModel.find_token_by_player_id(receiverID)
        if not sender_token or not receiver_token:
            print("player not found")
            return False
        # try to push to sender
        data = {
            "playerID": senderID,
            "title": "Private chat message",
            "content": "tap here to view"
        }
        payload = {
            "data": data,
            "to": sender_token
        }
        res = requests.post(cls.push_url,
                            headers = cls.header,
                            data = json.dumps(payload))
        if res.status_code != 200:
            return False
        # try to push to receiver
        data['playerID'] = receiverID
        payload['to'] = receiver_token
        res = requests.post(cls.push_url,
                            headers = cls.header,
                            data = json.dumps(payload))
        if res.status_code == 200:
            return True

        print(res)
        return False

    # subscribe player to club chat topic
    @classmethod
    def add_player_to_club_chat(cls,playerID,clubID):
        print("add player<{}> to club<{}>.".format(playerID,clubID))
        token = TokenModel.find_token_by_player_id(playerID)
        if token:
            print(token.json())
            url = "https://iid.googleapis.com/iid/v1/{}/rel/topics/club_{}".format(token.instanceToken,clubID)
            res = requests.post(url, headers=cls.header)
            if res.status_code == 200:
                return True
        return False

    # subscribe player to tournament chat topic
    @classmethod
    def add_player_to_tournament_chat(cls,playerID,clubID,tournamentID):
        token = TokenModel.find_token_by_player_id(playerID)
        if token:
            print(token.json())
            url = "https://iid.googleapis.com/iid/v1/{}/rel/topics/club_{}_tournament_{}".format(token.instanceToken,clubID,tournamentID)
            res = requests.post(url, headers=cls.header)
            if res.status_code == 200:
                return True
        return False

    # unsubscribe player to club chat topic
    @classmethod
    def remove_player_from_club_chat(cls,playerID,clubID):
        print("remove player<{}> from club<{}> chat.".format(playerID,clubID))
        token = TokenModel.find_token_by_player_id(playerID)
        if token:
            print(token.json())
            url = "https://iid.googleapis.com/iid/v1:batchRemove"
            payload = {
                "to": "/topics/club_{}".format(clubID),
                "registration_tokens": [token.instanceToken]
            }
            res = requests.post(url, headers=cls.header,data=json.dumps(payload))
            if res.status_code == 200:
                return True
        return False

    # subscribe player to tournament chat topic
    @classmethod
    def remove_player_from_tournament_chat(cls,playerID,clubID,tournamentID):
        token = TokenModel.find_token_by_player_id(playerID)
        if token:
            print(token.json())
            url = "https://iid.googleapis.com/iid/v1:batchRemove"
            payload = {
                "to": "/topics/club_{}_tournament_{}".format(clubID,tournamentID),
                "registration_tokens": [token.instanceToken]
            }
            res = requests.post(url, headers=cls.header,data=json.dumps(payload))
            if res.status_code == 200:
                return True
        return False
