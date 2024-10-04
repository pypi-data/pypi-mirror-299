from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums import (
    DeploymentType,
    ExplainerType,
    ModelFrameworkVersion,
    ModelType,
    TransformerType,
)


class CreateDeploymentBase(BaseModel):
    """Class that contains the base options for creating a Deployment"""

    name: str
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    repository_id: str
    """str: uuid of the Repository"""
    branch_name: str
    """str: the branch name of the Repository to deploy"""
    commit: Optional[str] = None
    """str, optional: the commit sha on the selected branch. If no commit is provided, the latest commit will be used"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""
    model_type: ModelType
    """int: enum value from ModelType class"""
    model_framework_version: Optional[ModelFrameworkVersion] = None
    """string: enum value from ModelFrameworkVersion class"""
    explainer_type: Optional[ExplainerType] = ExplainerType.NO_EXPLAINER
    """int, optional: enum value from ExplainerType class. Defaults to 0 (no explainer)"""
    transformer_type: Optional[TransformerType] = TransformerType.NO_TRANSFORMER
    """int, optional: enum value from TransformerType class. Defaults to 0 (no transformer)"""

    def to_request_body(self, deployment_type: DeploymentType) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "deploymentType": deployment_type.value,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "contractPath": self.contract_path,
            "modelType": self.model_type.value,
            "modelFrameworkVersion": self.model_framework_version,
            "explainerType": self.explainer_type.value,
            "transformerType": self.transformer_type.value,
        }
