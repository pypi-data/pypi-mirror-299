from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums import DeploymentType


class CreateNonStandardDeploymentBase(BaseModel):
    """Class that contains the base options for creating a Deployment"""

    name: str
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    repository_id: Optional[str] = None
    """str, optional: uuid of the Repository"""
    branch_name: Optional[str] = None
    """str, optional: the branch name of the Repository to deploy"""
    commit: Optional[str] = None
    """str, optional: the commit sha on the selected branch. If no commit is provided, the latest commit will be used"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""

    def to_request_body(self, deployment_type: DeploymentType) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "deploymentType": deployment_type.value,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "contractPath": self.contract_path,
        }
