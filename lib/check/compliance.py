import sys

from lib.check.compliance_models import Compliance_Base_Model, Compliance_Requirement
from lib.logger import logger


def update_compliance_metadata_with_compliance(
    bulk_compliance_frameworks: dict, bulk_checks_metadata: dict
):
    """Update the check metadata model with the compliance framework"""
    try:
        for check in bulk_checks_metadata:
            check_compliance = []
            for framework in bulk_compliance_frameworks.values():
                compliance_requirements = []
                compliance = Compliance_Base_Model

                for requirement in framework.Requirements:
                    if check in requirement.Checks:
                        # Create the Compliance_Requirement
                        requirement = Compliance_Requirement(
                            Id=requirement.Id,
                            Description=requirement.Description,
                            Attributes=requirement.Attributes,
                            Checks=requirement.Checks,
                        )
                        # For the check metadata we don't need the "Checks" key
                        delattr(requirement, "Checks")
                        # Include the requirment into the check's framework requirements
                        compliance_requirements.append(requirement)
                        # Create the Compliance_Model
                        compliance = Compliance_Base_Model(
                            Framework=framework.Framework,
                            Version=framework.Version,
                            Requirements=compliance_requirements,
                        )
                # Include the compliance framework for the check
                check_compliance.append(compliance)
            # Save it into the check's metadata
            bulk_checks_metadata[check].Compliance = check_compliance
    except Exception as e:
        logger.critical(f"{e.__class__.__name__} -- {e}")
        sys.exit()
