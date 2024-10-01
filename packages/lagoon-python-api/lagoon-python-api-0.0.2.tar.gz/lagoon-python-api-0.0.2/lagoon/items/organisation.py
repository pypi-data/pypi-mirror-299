# -*- coding: utf-8 -*-
from ..item import Item


class Organisation(Item):
    """
    This class describes an Organisation object child of Item class.
    """

    organisation_view = {
        "_id": "item._id",
        "_key": "item._key",
        "_rev": "item._rev",
        "type": "item.type",
        "createdAt": "item.createdAt",
        "updatedAt": "item.updatedAt",
        "createdBy": "item.createdBy",
        "updatedBy": "item.updatedBy",
        "data": "item.data",
        "properties": "FIRST(# -($Child)> 0,1 $Properties SORT null VIEW item)",
        "talents": "FIRST(# -($Child)> 0,1 item.data.name IN ['Talents', 'People'] SORT null VIEW item)",
        "applicants": "FIRST(# -($Child)> 0,1 item.data.name == 'Applicants' SORT null VIEW item)",
        "licenses": "FIRST(# -($Child)> 0,1 item.data.name == 'Licenses' SORT null VIEW item)",
        "hardware": "FIRST(# -($Child)> 0,1 item.data.name == 'Hardware' SORT null VIEW item)",
        "projects": "FIRST(# -($Child)> 0,1 item.data.name == 'Projects' SORT null VIEW item)",
        "buildings": "FIRST(# -($Child)> 0,1 item.data.name == 'Buildings' SORT null VIEW item)",
        "teams": "FIRST(# -($Child)> 0,1 item.data.name == 'Teams' SORT null VIEW item)",
    }

    def __call__(self, organisationData = {}):
        """
        Constructor of the Organisation class

        :param      organisationData:  The organisation data
        :type       organisationData:  dictionary
        """
        inst = super(Organisation, self).__call__(organisationData)
        inst.properties = None
        if ('properties' in organisationData):
            inst.properties = self.parent.item(organisationData['properties'])

        inst.talents = None
        if ('talents' in organisationData):
            inst.talents = self.parent.item(organisationData['talents'])

        inst.applicants = None
        if ('applicants' in organisationData):
            inst.applicants = self.parent.item(organisationData['applicants'])

        inst.licenses = None
        if ('licenses' in organisationData):
            inst.licenses = self.parent.item(organisationData['licenses'])

        inst.hardware = None
        if ('hardware' in organisationData):
            inst.hardware = self.parent.item(organisationData['hardware'])

        inst.projects = None
        if ('projects' in organisationData):
            inst.projects = self.parent.item(organisationData['projects'])

        inst.buildings = None
        if ('buildings' in organisationData):
            inst.buildings = self.parent.item(organisationData['buildings'])

        inst.teams = None
        if ('teams' in organisationData):
            inst.teams = self.parent.item(organisationData['teams'])

        return inst

    def get(self, organisationKey):
        """
        Get an organisation by its key

        :param      organisationKey:  The key of the organisation
        :type       organisationKey:  string

        :returns:   Organisation object
        :rtype:     :class:`~lagoon.items.organisation.Organisation`
        """
        meshql = f"# 0,1 $Organisation AND item._key == '{organisationKey}' VIEW $view"
        aliases = {"view": self.organisation_view}
        results = self.parent.query(meshql, aliases=aliases)

        if len(results) == 0:
            return None
        return self.parent.organisation(results[0])

    # Lagoon methods
    def get_organisations(self, limit=200, offset=None):
        """
        Get all organisations

        :param      limit:   Maximum limit number of returned organisations
        :type       limit:   integer
        :param      offset:  Number of skipped organisations. Used for pagination
        :type       offset:  integer

        :returns:   List of Organisation objects
        :rtype:     List of :class:`~lagoon.items.organisation.Organisation`
        """

        meshql = f"# {offset or 0},{limit or 50} $Organisation VIEW $view"
        aliases = {"view": self.organisation_view}

        result = self.parent.query(meshql, aliases=aliases)
        result = [self.parent.organisation(org) for org in result]
        return result

    def get_projects(self, offset = 0, limit = 200):
        """
        Get all projects of the organisation

        :param      offset:  Number of skipped projects. Used for pagination
        :type       offset:  integer
        :param      limit:   Maximum limit number of returned projects
        :type       limit:   integer

        :returns:   List of Project object
        :rtype:     List of :class:`~lagoon.items.project.Project`
        """

        meshql = f"# -($Child)> {offset},{limit} $Project VIEW item"
        projects = self.projects.traverse(meshql)
        projects = [self.parent.cast(project) for project in projects]
        return projects

    def get_talents(self, offset = 0, limit = 200):
        """
        Get all talents of the organisation

        :param      offset:  Number of skipped talents. Used for pagination
        :type       offset:  integer
        :param      limit:   Maximum limit number of returned talents
        :type       limit:   integer

        :returns:   List of Person object
        :rtype:     List of :class:`~lagoon.items.person.Person`
        """

        meshql = f"# -($Child)> {offset},{limit} $Person VIEW item"
        talents = self.talents.traverse(meshql)
        talents = [self.parent.person(talent) for talent in talents]
        return talents

    def get_software(self, offset = 0, limit = 200):
        """
        Get all software of the organisation

        :param      offset:  Number of skipped software. Used for pagination
        :type       offset:  integer
        :param      limit:   Maximum limit number of returned software
        :type       limit:   integer

        :returns:   List of Software object
        :rtype:     List of :class:`~lagoon.items.software.Software`
        """

        meshql = f"# -($Child)> {offset},{limit} $Software VIEW item"
        software = self.licenses.traverse(meshql)
        software = [self.parent.software(soft) for soft in software]
        return software

    def get_hardware(self, offset = 0, limit = 200):
        """
        Get all hardware of the organisation

        :param      offset:  Number of skipped hardware. Used for pagination
        :type       offset:  integer
        :param      limit:   Maximum limit number of returned hardware
        :type       limit:   integer

        :returns:   List of Hardware object
        :rtype:     List of :class:`~lagoon.items.hardware.Hardware`
        """

        meshql = f"# -($Child)> {offset},{limit} $Hardware VIEW item"
        hardware = self.hardware.traverse(meshql)
        hardware = [self.parent.hardware(hw) for hw in hardware]
        return hardware


    # Low level methods

    def get_member_by_email(self, email):
        """
        Get an exising member of the organisation by his/her email

        :returns:   User object
        :rtype:     :class:`~lagoon.items.user.User`
        """
        member = None
        members = self.get_all_members()
        filtered = [member for member in members if member.data.email == email]

        if len(filtered) > 0:
            member = filtered[0]

        return member

    def get_all_members(self, limit=200, offset=None):
        """
        Gets all members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~lagoon.items.user.User`
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        result = self.do_request(
            "GET", "organisations/{0}/members/all".format(self._key), params=params
        )
        result = [self.parent.user(user) for user in result]
        return result

    def get_active_members(self, limit=200, offset=None):
        """
        Gets all active members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~lagoon.items.user.User`
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        result = self.do_request(
            "GET", "organisations/{0}/members/active".format(self._key), params=params
        )
        result = [self.parent.user(user) for user in result]
        return result

    def get_inactive_members(self, limit=200, offset=None):
        """
        Gets all inactive members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~lagoon.items.user.User`
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        result = self.do_request(
            "GET", "organisations/{0}/members/inactive".format(self._key), params=params
        )
        result = [self.parent.user(user) for user in result]
        return result

    def add_member(self, user_key):
        """
        Add an existing user in your organisation

        :param      user_key:  The user key of the user to add in the organisation
        :type       user_key:  string

        :returns:   User object
        :rtype:     :class:`~lagoon.items.user.User`
        """

        payload = dict(userKey=user_key)

        member = self.do_request(
            "POST",
            "organisations/{organisationKey}/members".format(organisationKey=self._key),
            json=payload,
        )

        member = self.parent.cast(member)

        return member

    def create_member(self, email, name=None, lagoon_url=None):
        """
        Create a new member in your organisation

        :param      email:        The email of the new member
        :type       email:        string
        :param      name:         The name of the new member
        :type       name:         string, optional
        :param      lagoon_url: The Lagoon interface url. Useful if API url is not the same as Lagoon interface.
        :type       lagoon_url: string, optional (default is api_url used during module initialisation)

        :returns:   User object
        :rtype:     :class:`~lagoon.items.user.User`
        """

        member = self.parent.create_user(email, name, lagoon_url)

        self.add_member(member._key)

        return member
