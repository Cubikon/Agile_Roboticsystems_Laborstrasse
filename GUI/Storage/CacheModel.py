class CacheModel:
    def __init__(self, experiment_id, language):
        self.experiment_id = experiment_id
        self.language = language

    def __repr__(self):
        return f"CacheModel(experiment_id={self.experiment_id}, language={self.language})"

    def __str__(self):
        return f"CacheModel(experiment_id={self.experiment_id}, language={self.language})"
