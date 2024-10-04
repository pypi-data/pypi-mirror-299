from typing import Dict, Optional

from deeploy.enums import DeploymentType
from deeploy.models import CreateNonStandardDeploymentBase


class CreateExternalDeployment(CreateNonStandardDeploymentBase):
    """Class that contains the options for creating a external deployment"""
    
    url: str
    """str, optional: url endpoint of external deployment"""
    username: Optional[str] = None
    """str, optional: username for basic authentication"""
    password: Optional[str] = None
    """str, optional: password/bearer token for basic/bearer authentication"""
    
    def to_request_body(self) -> Dict:
        if self.username is not None and self.password is None:
            raise Exception("Basic authentication requires both username and password")
        return {
            **super().to_request_body(deployment_type= DeploymentType.EXTERNAL),
            "url": self.url,
            "username": self.username,
            "password": self.password,
        }
