class Goalie:
    def __init__(
        self,
        name,
        age,
        team,
        position,
        games_played,
        games_started,
        wins,
        losses,
        overtime_losses,
        goals_allowed,
        shots_against,
        saves,
        save_percentage,
        goals_against_average,
        shutouts,
        goalie_point_shares,
        minutes,
        quality_starts,
        quality_starts_percentage,
        really_bad_starts,
        goals_allowed_percentage,
        goals_saved_above_average,
        goals,
        assists,
        points,
        penalty_minutes,
    ):
        self.name = name
        self.age = age
        self.team = team
        self.position = position
        self.games_played = games_played
        self.games_started = games_started
        self.wins = wins
        self.losses = losses
        self.overtime_losses = overtime_losses
        self.goals_allowed = goals_allowed
        self.shots_againts = shots_against
        self.saves = saves
        self.save_percentage = save_percentage
        self.goals_against_average = goals_against_average
        self.shutouts = shutouts
        self.goalie_point_shares = goalie_point_shares
        self.minutes = minutes
        self.quality_starts = quality_starts
        self.quality_starts_percentage = quality_starts_percentage
        self.really_bad_starts = really_bad_starts
        self.goals_allowed_percentage = goals_allowed_percentage
        self.goals_saved_abover_average = goals_saved_above_average
        self.goals = goals
        self.assists = assists
        self.points = points
        self.penalty_minutes = penalty_minutes
