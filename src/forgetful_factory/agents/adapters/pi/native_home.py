"""The native Pi home the user consented to share, saved in .factory/pi-profile.json."""
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.resource_files import read_generated_json

FACTORY_DIRECTORY = '.factory'
PI_PROFILE_FILE = 'pi-profile.json'


def saved_pi_home(workspace: Path) -> str:
    try:
        data = read_generated_json(workspace / FACTORY_DIRECTORY / PI_PROFILE_FILE)
        directory = data['agent_directory']
        if (data['shared_profile_consent'] is not True or not isinstance(directory, str)
                or not Path(directory).is_absolute() or '\x00' in directory
                or Path(directory).is_relative_to(workspace / FACTORY_DIRECTORY)):
            raise ValueError('Invalid consent')
        return directory
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise FactoryError('Shared Pi profile consent is missing or invalid. '
                           'Review .factory/pi-profile.json if it exists; '
                           'use init --finalize to approve missing consent for saved setup.'
                           ) from error
