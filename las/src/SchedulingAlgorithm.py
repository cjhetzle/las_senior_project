import abc


class SchedulingAlgorithm(abc.ABC):
    @abc.abstractmethod
    def schedule(self, jobs, load):
        pass
