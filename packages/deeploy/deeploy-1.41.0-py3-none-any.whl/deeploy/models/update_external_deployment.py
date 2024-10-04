from typing import Dict, Optional

from deeploy.models import UpdateNonStandardDeploymentBase


class UpdateExternalDeployment(UpdateNonStandardDeploymentBase):
    """Class that contains the options for updating a External Deployment"""

    url: Optional[str] = None
    """str, optional: url endpoint of external deployment"""
    username: Optional[str] = None
    """str, optional: username for basic authentication"""
    password: Optional[str] = None
    """str, optional: password/bearer token for basic/bearer authentication"""

    def to_request_body(self) -> Dict:
        if self.username is not None and self.password is None:
            raise Exception("Basic authentication requires both username and password")
        request_body = {
            **super().to_request_body(),
            "url": self.url,
            "username": self.username,
            "password": self.password,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}