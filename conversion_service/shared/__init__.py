import enum

from rq.job import JobStatus as RQJobStatus


class ChoicesEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return tuple((member.value, member.value) for member in cls)


class MostSignificantEnumMixin(enum.Enum):
    @staticmethod
    def _precedence_list():
        raise NotImplementedError

    @classmethod
    def most_significant(cls, status_list):
        if len(status_list) > 0:
            return min(status_list, key=cls._precedence_list().index)
        else:
            return None


class JobStatus(ChoicesEnum):
    ERROR = 'error'
    NEW = 'new'
    QUEUED = 'queued'
    STARTED = 'started'
    DONE = 'done'

    @staticmethod
    def _precedence_list():
        return [JobStatus.ERROR, JobStatus.NEW, JobStatus.QUEUED, JobStatus.STARTED, JobStatus.DONE]

rq_job_status_mapping = {
    RQJobStatus.QUEUED: JobStatus.QUEUED,
    RQJobStatus.FINISHED: JobStatus.DONE,
    RQJobStatus.FAILED: JobStatus.ERROR,
    RQJobStatus.STARTED: JobStatus.STARTED,
    RQJobStatus.DEFERRED: JobStatus.QUEUED,
}


class ConversionProgress(ChoicesEnum, MostSignificantEnumMixin):
    ERROR = 'error'
    NEW = 'new'
    RECEIVED = 'received'
    STARTED = 'started'
    SUCCESSFUL = 'successful'

    @staticmethod
    def _precedence_list():
        return [ConversionProgress.ERROR, ConversionProgress.NEW, ConversionProgress.RECEIVED, ConversionProgress.STARTED, ConversionProgress.SUCCESSFUL]
