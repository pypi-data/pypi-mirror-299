from typing import Dict

from deeploy.enums import DeploymentType
from deeploy.models import CreateNonStandardDeploymentBase


class CreateRegistrationDeployment(CreateNonStandardDeploymentBase):
    """Class that contains the options for creating a registration deployment"""

    def to_request_body(self) -> Dict:
        return {
            **super().to_request_body(deployment_type= DeploymentType.REGISTRATION)
        }
