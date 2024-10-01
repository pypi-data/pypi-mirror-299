# -*- coding: utf-8 -*-
import os
import mimetypes

from .auth import LagoonAuth
from .events import Events
from .item import Item
from .edge import Edge
from .tools import evaluate
from .items.bot import Bot
from .items.user import User
from .items.person import Person
from .items.project import Project
from .items.software import Software
from .items.hardware import Hardware
from .items.product import Product
from .items.usergroup import Usergroup
from .items.organisation import Organisation
from .element import Element
from .events import Event
from .utils import Utils


import requests

import sys
if sys.version_info[0] > 2:
    from urllib.parse import urljoin, urlparse
else:
    from urlparse import urljoin, urlparse

import json
import logging
logger=logging.getLogger(__name__)


class Lagoon(object):
    """
    This class describes the main class of Lagoon

    :param api_url: Specify the URL of the API.
    :type api_url: string
    :param token: Specify the authentication token, to avoid :func:`~lagoon.lagoon.Lagoon.signin`
    :type token: string, optional
    :param api_version: Specify the API version you want to use (default : `v1`).
    :type api_version: string, optional
    :param domain: Specify the domain used for unauthenticated requests. Mainly for Lagoon Fatfish Lab dev or local Lagoon server without DNS
    :type domain: string, optional
    :param strict_dotmap: Specify if the dotmap should create new property dynamically (default : `False`). Set to `True` to have default Python behaviour like on Dict()
    :type strict_dotmap: boolean, optional

    :var token: Get the current token (populated after a first :func:`~lagoon.lagoon.Lagoon.signin`)
    :var edge: Access to Edge class
    :vartype edge: :class:`~lagoon.edge.Edge`
    :var project: Access to Project subclass
    :vartype project: :class:`~lagoon.items.project.Project`
    :var bot: Access to Bot subclass
    :vartype bot: :class:`~lagoon.items.bot.Bot`
    :var user: Access to User subclass
    :vartype user: :class:`~lagoon.items.user.User`
    :var usergroup: Access to Usergroup subclass
    :vartype usergroup: :class:`~lagoon.items.usergroup.Usergroup`
    :var organisation: Access to Organisation subclass
    :vartype organisation: :class:`~lagoon.items.organisation.Organisation`
    :var utils: Access to Utils class
    :vartype utils: :class:`~lagoon.utils.Utils`
    """

    def __init__(self, api_url='', token=None, api_version='v1', domain=None, strict_dotmap=False):
        """
        Constructs a new instance.
        """
        # Session
        self.session=requests.Session()

        self.api_url=api_url
        self.api_version=api_version
        self.token=token
        self.domain=domain
        self.strict_dotmap=strict_dotmap

        # Classes
        self.events=Events(parent=self)
        self.element=Element(parent=self)
        self.item=Item(parent=self)
        self.edge=Edge(parent=self)
        self.utils=Utils()
        # SubClasses
        self.bot=Bot(parent=self)
        self.user=User(parent=self)
        self.usergroup=Usergroup(parent=self)
        self.organisation=Organisation(parent=self)
        self.person=Person(parent=self)
        self.software=Software(parent=self)
        self.hardware=Hardware(parent=self)
        self.product=Product(parent=self)
        self.project=Project(parent=self)
        self.event=Event(parent=self)

    def do_request(self, *args, **kwargs):
        """
        Execute a request to the API

        :param      args:    Parameters used to send the request : HTTP verb, API endpoint
        :type       args:    tuple
        :param      kwargs:  Headers, data and parameters used for the request
        :type       kwargs:  dictionary

        :returns:   Request response
        :rtype:     List or dictionary
        """
        token=self.token

        stream=False
        if 'stream' in kwargs:
            stream=kwargs['stream']

        decoding=True
        if 'decoding' in kwargs:
            decoding=kwargs.pop('decoding')

        headers=None
        if 'headers' in kwargs:
            headers=kwargs.pop('headers')
            if headers is not None:
                headers.update(dict(authorization=token))

        args=list(args)
        typ=args[0]
        path = self.api_url

        if len(args) > 1:
            is_files = args[1].find('/files/') >= 0
            if (is_files):
                path = urljoin(path, args[1])
            else:
                path = urljoin(path, '{api_version}/{endpoint}'.format(
                    api_version=self.api_version,
                    endpoint=args[1]
                ))
        else:
            path = urljoin(path, self.api_version)

        logger.debug('Send request : %s %s', typ, path)
        response=self.session.request(typ, path, headers=headers, auth=LagoonAuth(self.token, self.domain), **kwargs)

        evaluate(response)
        if not stream:
            if decoding:
                response=response.json()

        return response

    def cast(self, data={}):
        """
        Creates an item or edge instance from a dictionary

        :param      data:         The object item or edge from Lagoon API
        :type       data:         dictionary

        :returns:   Instance of Edge or Item or items subclass
        :rtype:     :class:`~lagoon.edge.Edge` | :class:`~lagoon.item.Item` : [:class:`~lagoon.items.asset.Asset` | :class:`~lagoon.items.project.Project` | :class:`~lagoon.items.shot.Shot` | :class:`~lagoon.items.task.Task` | :class:`~lagoon.items.template.Template` | :class:`~lagoon.items.user.User` | :class:`~lagoon.items.usergroup.Usergroup`]
        """
        value=data
        #As Entity
        if data and '_id' in data.keys():
            id=data.get('_id')
            cls=None
            #As Item
            if id.split('/')[0]=='items':
                type=data.get('type')
                if type=='Project':
                    cls=self.project
                elif type=='User':
                    cls=self.user
                elif type=='Usergroup':
                    cls=self.usergroup
                elif type=='Organisation':
                    cls=self.organisation
                elif type=='Person':
                    cls=self.person
                elif type=='Software':
                    cls=self.software
                elif type=='Hardware':
                    cls=self.hardware
                elif type=='Product':
                    cls=self.product
                else:
                    cls=self.item
            #As Edge
            elif id.split('/')[0]=='connections':
                cls=self.edge
            #As Event
            elif id.split('/')[0]=='events':
                cls=self.event
            if cls is not None:
                value=cls(data=data)

        return value

    def signin(self, email='', password=''):
        """
        Sign in a user with its email and password

        :param      email:     The email of the user
        :type       email:     string
        :param      password:  The password of the user
        :type       password:  string
        """
        return self.user.signin(email=email, password=password)

    def signout(self):
        """
        Sign out current user by clearing the stored authentication token

        .. note::
            After a :func:`~lagoon.lagoon.Lagoon.signout`, you need to use a :func:`~lagoon.lagoon.Lagoon.signin` before sending authenticated requests

        :returns: None
        """
        logger.info('Disconnect current user')
        logger.debug('Clear authentication token for logout')
        self.user.signout()

    def me(self):
        """
        Alias of :func:`~lagoon.items.user.User.get_current`


        :returns:   A :class:`~lagoon.items.user.User` instance of the connected user.
        :rtype:     :class:`~lagoon.items.user.User` object
        """
        result=self.user.get_current()
        return result
        return self.get_current_user()

    def mine(self):
        """
        Alias of :func:`~lagoon.items.user.User.get_profile`


        :returns:   User, Usergroups and Organisations object
        :rtype:     Dict {user: :class:`~lagoon.items.user.User`, usergroups: [:class:`~lagoon.items.usergroup.Usergroup`], organisations: [:class:`~lagoon.items.organisation.Organisation`]}
        """
        return self.user.get_profile()

    def get_organisations(self, limit=200, offset=None):
      """
      List all organisations

      :param      limit:   The maximum number of organisations to retrieve (default: 200)
      :type       limit:   int, optional
      :param      offset:  The offset to start retrieving organisations from (default: None)
      :type       offset:  int, optional

      :returns:   List of organisations
      :rtype:     List of :class:`~lagoon.items.organisation.Organisation`
      """
      return self.organisation.get_organisations(limit=limit, offset=offset)

    def get_server_status(self):
        """
        Gets the server status.

        :returns:   The server status
        :rtype:     dictionary
        """
        result=self.do_request('GET', 'status')
        return result

    def ping (self):
        """
        Ping Lagoon server

        :returns: Ping response: pong
        :rtype:   string
        """
        ping = self.do_request('GET', 'ping', decoding=False)
        return ping.text

    def get_users (self):
        """
        Get all users

        :returns: List of all users
        :rtype:   List of :class:`~lagoon.items.user.User`
        """

        users = self.do_request('GET', 'users')

        users = [self.cast(user) for user in users]
        return users

    def create_user (self, email, name=None, lagoon_url=None):
        """
        Create a new user

        :param      email:  The email of the new user
        :type       email:  string
        :param      name:   The name of the new user
        :type       name:   string, optional
        :param      lagoon_url: The Lagoon interface url. Useful if API url is not the same as Lagoon interface.
        :type       lagoon_url: string, optional (default is api_url used during module initialisation)

        :returns:   User object
        :rtype:     :class:`~lagoon.items.user.User`
        """

        payload = dict(email=email)
        if name != None:
            payload['name'] = name

        headers = {
            'origin': lagoon_url or self.api_url
        }

        user = self.do_request(
            'POST', 'users', json=payload, headers=headers)

        user = self.cast(user)
        return user


    def forgot_password(self, email, lagoon_url=None):
        """
        Start forgot password procedure. User will receive an email to reset its password.

        :param      email:        Email of the user who forgot its password
        :type       email:        string
        :param      lagoon_url: The Lagoon interface url. Useful if API url is not the same as Lagoon interface.
        :type       lagoon_url: string, optional (default is api_url used during module initialisation)

        :returns: True or False
        :rtype: boolean
        """

        if (email is not None):
            data = {
                'email': email
            }
            headers = {
                'origin': lagoon_url or self.api_url
            }
            self.do_request(
            'POST', 'forgot', json=data, headers=headers)
            return True

    def upload_file(self, path=''):
        """
        Uploads a file on the server

        .. note::
            The file is just uploaded to Lagoon. The metadata are not saved on any item. Use :func:`~lagoon.item.Item.update_data` to save them on an item.
            You can also directly upload a file on an item with :func:`~lagoon.item.Item.upload_file`.

        :param      path:  The path of the file to upload
        :type       path:  string

        :returns:   The file metadata on Lagoon
        :rtype:     dictionary
        """
        logger.debug('Upload file : %s', path)

        file = open(path, 'rb')
        filename = os.path.basename(path)
        file_content_type = mimetypes.guess_type(filename)

        files=dict(file=(filename, file, file_content_type))
        result = self.do_request('POST', 'upload', files=files)
        file.close()
        return result

    def query(self, meshql='', aliases={}):
        """
        Query entities

        .. tip::
            For better performances, we advice you to use the function :func:`~lagoon.item.Item.traverse`

        :param      meshql:        The meshql string
        :type       meshql:        string
        :param      aliases:       The aliases used in the meshql query
        :type       aliases:       dictionary

        :returns:   List of item, edge or VIEW used in the meshql query
        :rtype:     list
        """
        logger.debug('Send query : meshql : %s / aliases : %r',
                     meshql, aliases)
        data=dict(query=meshql, aliases=aliases)
        result=self.do_request('POST', 'query', json=data)
        return result

    def get_file(self, file_path):
        """
        Get stored file on Lagoon server

        :param      file_path:     The file path from item property (Exemple: `/files/file_id.jpg`)
        :type       file_path:     string

        :returns:   The file
        :rtype:     list
        """

        response = self.do_request('GET', file_path, decoding=False)
        return response.content
