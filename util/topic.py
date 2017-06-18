from models.player import PlayerModel
from models.club import ClubModel
from models.token import TokenModel
import requests

class Topic:

    # return None if something is wrong
    @classmethod
    def add_player_to_club_chat(cls,playerID,clubID):
        token = TokenModel.find_token_by_player_id(playerID)
        if token:
            print(token.json())
            headers = {
                'Authorization': 'key=AAAAUUkuPO4:APA91bHM-4XdsAEnsLYLOEkSDQP1DZp4lwiRwOaOhq9FQ8I7ONpxzm9hVU_jcWtzx6EsysU2wcUF1TpqR43uCZsu3aIvWuCvGloJLeVmfIiHgke7qqlZQ-xejIvlu8wRcJ0tC8IJJY8E'
                    }
            url = "https://iid.googleapis.com/iid/v1/" + token.instanceToken + "/rel/topics/club_chat_" + clubID
            print("url="+url)
            res = requests.post(url, headers=headers)
            if res.status_code == 200:
                print(res)
                return True
        return False

    @classmethod
    def add_player_to_tournament_chat(cls,playerID,clubID,tournamentID):
        pass
