"""
Tools to create programs-related data for use in bok choy tests.
"""
from collections import namedtuple
import json

import requests

from . import PROGRAMS_STUB_URL
from .config import ConfigModelFixture
from openedx.core.djangoapps.programs.tests import factories


# TODO: Use factories directly instead of using this namedtuple as a proxy.
FakeProgram = namedtuple('FakeProgram', ['name', 'status', 'org_key', 'course_id', 'program_id'])


class ProgramsFixture(object):
    """
    Interface to set up mock responses from the Programs stub server.
    """

    def install_programs(self, fake_programs, single=False):
        """
        Sets the response data for Programs API endpoints.

        At present, `fake_programs` must be a iterable of FakeProgram named tuples.
        """
        if single:
            data = fake_programs[0]
            program = self._create_program(data)

            path = 'programs/{}'.format(data.program_id)
            api_result = program
        else:
            programs = [self._create_program(data) for data in fake_programs]

            path = 'programs'
            api_result = {'results': programs}

        requests.put(
            '{}/set_config'.format(PROGRAMS_STUB_URL),
            data={path: json.dumps(api_result)},
        )

    def _create_program(self, data):
        """Create a fake program.

        Arguments:
            data (FakeProgram): A named tuple containing data used to create a fake program.
        """
        run_mode = factories.RunMode(course_key=data.course_id)
        course_code = factories.CourseCode(run_modes=[run_mode])
        org = factories.Organization(key=data.org_key)

        program = factories.Program(
            name=data.name,
            status=data.status,
            organizations=[org],
            course_codes=[course_code]
        )

        return program


class ProgramsConfigMixin(object):
    """Mixin providing a method used to configure the programs feature."""
    def set_programs_api_configuration(self, is_enabled=False, api_version=1, api_url=PROGRAMS_STUB_URL,
                                       js_path='/js', css_path='/css'):
        """Dynamically adjusts the Programs config model during tests."""
        ConfigModelFixture('/config/programs', {
            'enabled': is_enabled,
            'api_version_number': api_version,
            'internal_service_url': api_url,
            'public_service_url': api_url,
            'authoring_app_js_path': js_path,
            'authoring_app_css_path': css_path,
            'cache_ttl': 0,
            'enable_student_dashboard': is_enabled,
            'enable_studio_tab': is_enabled,
            'enable_certification': is_enabled,
            'xseries_ad_enabled': is_enabled,
            'program_listing_enabled': is_enabled,
            'program_details_enabled': is_enabled,
        }).install()
