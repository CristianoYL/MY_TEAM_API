from db import db

class StatsModel(db.Model):
    __tablename__ = 'stats'
    # (tournamentID, clubID, playerID, attendance, appearance, start, goal,
    #   penalty, penaltyShootout, penaltyTaken, ownGoal, header, weakFootGoal
    #   otherGoal, assist, yellow, red, cleanSheet, penaltySaved)
    tournamentID = db.Column(db.Integer, db.ForeignKey('tournament.id'), primary_key=True)
    clubID = db.Column(db.Integer, db.ForeignKey('club.id'), primary_key=True)
    playerID = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    attendance = db.Column(db.Integer)
    appearance = db.Column(db.Integer)
    start = db.Column(db.Integer)
    goal = db.Column(db.Integer)
    penalty = db.Column(db.Integer)
    penaltyShootout = db.Column(db.Integer)
    penaltyTaken = db.Column(db.Integer)
    ownGoal = db.Column(db.Integer)
    header = db.Column(db.Integer)
    weakFootGoal = db.Column(db.Integer)
    otherGoal = db.Column(db.Integer)
    assist = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    red = db.Column(db.Integer)
    cleanSheet = db.Column(db.Integer)
    penaltySaved = db.Column(db.Integer)

    def __init__(self,tournamentID, clubID, playerID, attendance, appearance,
            start, goal,penalty, penaltyShootout, penaltyTaken, ownGoal,
            header,weakFootGoal,otherGoal,assist, yellow,red, cleanSheet, penaltySaved):
        self.tournamentID = tournamentID
        self.clubID = clubID
        self.playerID = playerID
        self.attendance = attendance
        self.appearance = appearance
        self.start = start
        self.goal = goal
        self.penalty = penalty
        self.penaltyShootout = penaltyShootout
        self.penaltyTaken = penaltyTaken
        self.ownGoal = ownGoal
        self.header = header
        self.weakFootGoal = weakFootGoal
        self.otherGoal = otherGoal
        self.assist = assist
        self.yellow = yellow
        self.red = red
        self.cleanSheet = cleanSheet
        self.penaltySaved = penaltySaved

    def json(self):
        return {
            'tournamentID' : self.tournamentID,
            'clubID' : self.clubID,
            'playerID' : self.playerID,
            'attendance' : self.attendance,
            'appearance' : self.appearance,
            'start' : self.start,
            'goal' : self.goal,
            'penalty' : self.penalty,
            'penaltyShootout' : self.penaltyShootout,
            'penaltyTaken' : self.penaltyTaken,
            'ownGoal' : self.ownGoal,
            'header' : self.header,
            'weakFootGoal' : self.weakFootGoal,
            'otherGoal' : self.otherGoal,
            'assist' : self.assist,
            'yellow' : self.yellow,
            'red' : self.red,
            'cleanSheet' : self.cleanSheet,
            'penaltySaved' : self.penaltySaved
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_stats(cls,tournamentID,clubID,playerID):
        return cls.query.filter_by(tournamentID=tournamentID,clubID=clubID,playerID=playerID).first()

    @classmethod
    def find_stats_by_tournament(cls,tournamentID):
        return cls.query.filter_by(tournamentID=tournamentID)

    @classmethod
    def find_stats_by_club(cls,clubID):
        return cls.query.filter_by(clubID=clubID)

    @classmethod
    def find_stats_by_player(cls,playerID):
        return cls.query.filter_by(playerID=playerID)

    @classmethod
    def find_tournament_total_stats(cls,tournamentID):
        tournament_stats = {
            'tournamentID' : tournamentID,
            'attendance' : 0,
            'appearance' : 0,
            'start' : 0,
            'goal' : 0,
            'penalty' : 0,
            'penaltyShootout' : 0,
            'penaltyTaken' : 0,
            'ownGoal' : 0,
            'header' : 0,
            'weakFootGoal' : 0,
            'otherGoal' : 0,
            'assist' : 0,
            'yellow' : 0,
            'red' : 0,
            'cleanSheet' : 0,
            'penaltySaved' : 0
        }
        total_stats = cls.query.filter_by(tournamentID=tournamentID)
        for stats in total_stats:
            tournament_stats['attendance'] += stats['attendance']
            tournament_stats['appearance'] += stats['appearance']
            tournament_stats['start'] += stats['start']
            tournament_stats['goal'] += stats['goal']
            tournament_stats['penalty'] += stats['penalty']
            tournament_stats['penaltyShootout'] += stats['penaltyShootout']
            tournament_stats['penaltyTaken'] += stats['penaltyTaken']
            tournament_stats['ownGoal'] += stats['ownGoal']
            tournament_stats['header'] += stats['header']
            tournament_stats['weakFootGoal'] += stats['weakFootGoal']
            tournament_stats['otherGoal'] += stats['otherGoal']
            tournament_stats['assist'] += stats['assist']
            tournament_stats['yellow'] += stats['yellow']
            tournament_stats['red'] += stats['red']
            tournament_stats['cleanSheet'] += stats['cleanSheet']
            tournament_stats['penaltySaved'] += stats['penaltySaved']
        return tournament_stats

    @classmethod
    def find_club_total_stats(cls,clubID):
        club_stats = {
            'clubID' : clubID,
            'attendance' : 0,
            'appearance' : 0,
            'start' : 0,
            'goal' : 0,
            'penalty' : 0,
            'penaltyShootout' : 0,
            'penaltyTaken' : 0,
            'ownGoal' : 0,
            'header' : 0,
            'weakFootGoal' : 0,
            'otherGoal' : 0,
            'assist' : 0,
            'yellow' : 0,
            'red' : 0,
            'cleanSheet' : 0,
            'penaltySaved' : 0
        }
        club_total_stats = cls.query.filter_by(tournamentID=tournamentID)
        for stats in club_total_stats:
            club_stats['attendance'] += stats['attendance']
            club_stats['appearance'] += stats['appearance']
            club_stats['start'] += stats['start']
            club_stats['goal'] += stats['goal']
            club_stats['penalty'] += stats['penalty']
            club_stats['penaltyShootout'] += stats['penaltyShootout']
            club_stats['penaltyTaken'] += stats['penaltyTaken']
            club_stats['ownGoal'] += stats['ownGoal']
            club_stats['header'] += stats['header']
            club_stats['weakFootGoal'] += stats['weakFootGoal']
            club_stats['otherGoal'] += stats['otherGoal']
            club_stats['assist'] += stats['assist']
            club_stats['yellow'] += stats['yellow']
            club_stats['red'] += stats['red']
            club_stats['cleanSheet'] += stats['cleanSheet']
            club_stats['penaltySaved'] += stats['penaltySaved']
        return club_stats

    @classmethod
    def find_player_total_stats(cls,playerID):
        player_stats = {
            'playerID' : playerID,
            'attendance' : 0,
            'appearance' : 0,
            'start' : 0,
            'goal' : 0,
            'penalty' : 0,
            'penaltyShootout' : 0,
            'penaltyTaken' : 0,
            'ownGoal' : 0,
            'header' : 0,
            'weakFootGoal' : 0,
            'otherGoal' : 0,
            'assist' : 0,
            'yellow' : 0,
            'red' : 0,
            'cleanSheet' : 0,
            'penaltySaved' : 0
        }
        total_stats = cls.query.filter_by(playerID=playerID)
        for stats in total_stats:
            player_stats['attendance'] += stats.attendance
            player_stats['appearance'] += stats.appearance
            player_stats['start'] += stats.start
            player_stats['goal'] += stats.goal
            player_stats['penalty'] += stats.penalty
            player_stats['penaltyShootout'] += stats.penaltyShootout
            player_stats['penaltyTaken'] += stats.penaltyTaken
            player_stats['ownGoal'] += stats.ownGoal
            player_stats['header'] += stats.header
            player_stats['weakFootGoal'] += stats.weakFootGoal
            player_stats['otherGoal'] += stats.otherGoal
            player_stats['assist'] += stats.assist
            player_stats['yellow'] += stats.yellow
            player_stats['red'] += stats.red
            player_stats['cleanSheet'] += stats.cleanSheet
            player_stats['penaltySaved'] += stats.penaltySaved
        return player_stats

    @classmethod
    def get_updated_stats(cls,prev_stats,vector):
        prev_stats.attendance += vector.attendance
        prev_stats.appearance += vector.appearance
        prev_stats.start += vector.start
        prev_stats.goal += vector.goal
        prev_stats.penalty += vector.penalty
        prev_stats.penaltyShootout += vector.penaltyShootout
        prev_stats.penaltyTaken += vector.penaltyTaken
        prev_stats.ownGoal += vector.ownGoal
        prev_stats.header += vector.header
        prev_stats.weakFootGoal += vector.weakFootGoal
        prev_stats.otherGoal += vector.otherGoal
        prev_stats.assist += vector.assist
        prev_stats.yellow += vector.yellow
        prev_stats.red += vector.red
        prev_stats.cleanSheet += vector.cleanSheet
        prev_stats.penaltySaved += vector.penaltySaved
        return prev_stats

    def save_to_db(self):   ## upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):   ## delete
        db.session.delete(self)
        db.session.commit()
