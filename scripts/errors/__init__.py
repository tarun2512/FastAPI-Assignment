class ErrorMessages:
    UNKNOWN = "Unknown Error occurred"
    ERR001 = "Configurations not available, please verify the database."
    ERR002 = "Data Not Found"
    ERR003 = "User Record Not Found"
    LOOKUPSERROR = "Could not find scadas configured in lookups for this app"
    SELECTEDDETAILSERROR = "Could not find selected all details"
    INCORRECTDETAILS = "Incorrect details"
    UNABLETOCONNECT = "Unable to connect with global catalog module"
    RULEDEFERROR = "Unable to get rule def details from global catalog module"
    CONFLICTSERROR = "Unable to detect conflicts"
    GLOBALCATALOGDETAILSERROR = "Unable to connect with get required details from global catalog module"
    CONNECTIONERROR = "Unable to connect to global catalogue to fetch material details {e}"
    WORKFLOWERROR = "workflow does not exist"
    USERMAPPINGERROR = "Failed to create user mapping"
    VERSIONERROR = "Failed to fetch available version list"
    PIPELINE_DETAILS_ERROR = "Unable to find pipeline details"


class JobCreationError(Exception):
    """
    Raised when a Job Creation throws an exception.

    Job Creation happens by adding a record to Mongo.
    """


class UnknownError(Exception):
    pass


class DuplicateSpaceNameError(Exception):
    pass


class KairosDBError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ImageValidation(Exception):
    pass


class ILensError(Exception):
    pass


class NameExists(Exception):
    pass


class InputRequestError(ILensError):
    pass


class IllegalTimeSelectionError(ILensError):
    pass


class DataNotFound(Exception):
    pass


class AuthenticationError(ILensError):
    """
    JWT Authentication Error
    """


class JWTDecodingError(Exception):
    pass


class DuplicateReportNameError(Exception):
    pass


class PathNotExistsException(Exception):
    pass


class ImplementationError(Exception):
    pass


class UserRoleNotFoundException(Exception):
    pass


class CustomAppError:
    FAILED_TO_SAVE = "Failed to save app"
