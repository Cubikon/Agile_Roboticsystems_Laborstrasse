class BorgSingleton:
    """
    Singleton Class to store shared data in Application Runtime
    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

class CurrentExperimentSingleton(BorgSingleton):
    def __init__(self, experiment_id=None):
        BorgSingleton.__init__(self)
        if experiment_id is not None:
            self.experiment_id = experiment_id

    def __str__(self):
        return f"CurrentExperimentSingleton(experiment_id={self.experiment_id})"

class ExperimentSingleton(BorgSingleton):
    """
    Singleton Class to store Experiment Data in Application Runtime
    """

    def __init__(self, firstname=None, lastname=None, exp_id=None, plasmids=None, plasmid_tubes=None, date=None):
        BorgSingleton.__init__(self)
        if firstname is not None:
            self.firstname = firstname
        if lastname is not None:
            self.lastname = lastname
        if exp_id is not None:
            self.experiment_id = exp_id
        if plasmids is not None:
            self.plasmids = plasmids
        if plasmid_tubes is not None:
            self.plasmid_tubes = plasmid_tubes
        if date is not None:
            self.date = date
        if not hasattr(self, 'plasmid_tubes') or self.plasmid_tubes is None:
            self.plasmid_tubes = {}

    def get_all_tubes(self):
        """
        Merge all the tubes into a list.
        """
        all_tubes = set()
        if self.plasmid_tubes is not None:
            for tubes in self.plasmid_tubes.values():
                all_tubes.update(tubes)
        return list(all_tubes)

    def clear_cache(self):
        """
        Clear the cache by setting all attributes to None.
        """
        self.firstname = None
        self.lastname = None
        self.experiment_id = None
        self.plasmids = None
        self.plasmid_tubes = {}
        self.date = None

    def __str__(self):
        return f'ExperimentSingleton(firstname={self.firstname}, lastname={self.lastname}, experimentId={self.experiment_id}, plasmids={self.plasmids}, tubes={self.plasmid_tubes}, date={self.date})'


class Tube(BorgSingleton):
    """
        Class to store Tube Data in Application Runtime
    """

    def __init__(self, qr_code=None, plasmid_nr=None):
        BorgSingleton.__init__(self)
        self.qr_code = qr_code
        self.plasmid_nr = plasmid_nr

    def __str__(self):
        return f'Tube(qr_code={self.qr_code}, plasmid_nr={self.plasmid_nr})'


class TubesSingleton(BorgSingleton):
    """
        Singleton Class to store Tubes Data in Application Runtime
    """

    def __init__(self):
        BorgSingleton.__init__(self)

        if not hasattr(self, 'tubes'):
            self.tubes = {}

    def add_tube(self, tube, qr_code, plasmid_nr):
        self.tubes[tube] = Tube(qr_code, plasmid_nr)

    def clear_cache(self):
        self.tubes = {}

    def __str__(self):
        return f'TubesSingleton(tubes={self.tubes})'


if __name__ == "__main__":
    # Use cases test, could be ignored
    borg = BorgSingleton()
    exp1 = ExperimentSingleton("Ujwal", "Subedi", "ujwal1", ['PHB30', 'PHB40'], {'PHB30': '4,5,6', 'PHB40': '1,2,3'},
                               '03.12.2023')
    print(exp1)
    exp2 = ExperimentSingleton("Wissam", "Alamareen", "wissam1", ['PHB35', 'PHB45'],
                               {'PHB35': '4,5,6', 'PHB45': '1,2,3'},
                               '03.12.2023')
    print(exp2)
    tubes1 = TubesSingleton()
    tubes1.add_tube('tube1', 'qr123', 'plasmid456')
    print(tubes1)

    tubes2 = TubesSingleton()
    print(tubes2)
    print(borg.__dict__.items())

    exp3 = ExperimentSingleton()
    print(exp3)
