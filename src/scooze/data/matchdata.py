import scooze.models.utils as model_utils


class MatchData:
    # TODO(#22): match data should ideally be a list of matches played and information about what was played against

    def __init__(self, wins: int = 0, losses: int = 0, draws: int = 0):
        self.wins = wins
        self.losses = losses
        self.draws = draws
