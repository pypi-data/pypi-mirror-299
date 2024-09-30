# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class AcceptOrganizationInvitationRequest(AbstractModel):
    """AcceptOrganizationInvitation request structure.

    """

    def __init__(self):
        r"""
        :param _Id: Invitation ID
        :type Id: int
        """
        self._Id = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id


    def _deserialize(self, params):
        self._Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AcceptOrganizationInvitationResponse(AbstractModel):
    """AcceptOrganizationInvitation response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class AddOrganizationNodeRequest(AbstractModel):
    """AddOrganizationNode request structure.

    """

    def __init__(self):
        r"""
        :param _ParentNodeId: Parent organizational unit ID
        :type ParentNodeId: int
        :param _Name: Organizational unit name
        :type Name: str
        """
        self._ParentNodeId = None
        self._Name = None

    @property
    def ParentNodeId(self):
        return self._ParentNodeId

    @ParentNodeId.setter
    def ParentNodeId(self, ParentNodeId):
        self._ParentNodeId = ParentNodeId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name


    def _deserialize(self, params):
        self._ParentNodeId = params.get("ParentNodeId")
        self._Name = params.get("Name")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddOrganizationNodeResponse(AbstractModel):
    """AddOrganizationNode response structure.

    """

    def __init__(self):
        r"""
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._NodeId = None
        self._RequestId = None

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._NodeId = params.get("NodeId")
        self._RequestId = params.get("RequestId")


class CancelOrganizationInvitationRequest(AbstractModel):
    """CancelOrganizationInvitation request structure.

    """

    def __init__(self):
        r"""
        :param _Id: Invitation ID
        :type Id: int
        """
        self._Id = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id


    def _deserialize(self, params):
        self._Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CancelOrganizationInvitationResponse(AbstractModel):
    """CancelOrganizationInvitation response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class CreateOrganizationRequest(AbstractModel):
    """CreateOrganization request structure.

    """

    def __init__(self):
        r"""
        :param _OrgType: Organization type; currently its value is fixed as `1`
        :type OrgType: int
        """
        self._OrgType = None

    @property
    def OrgType(self):
        return self._OrgType

    @OrgType.setter
    def OrgType(self, OrgType):
        self._OrgType = OrgType


    def _deserialize(self, params):
        self._OrgType = params.get("OrgType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateOrganizationResponse(AbstractModel):
    """CreateOrganization response structure.

    """

    def __init__(self):
        r"""
        :param _OrgId: Organization ID
        :type OrgId: int
        :param _Nickname: Creator's name
        :type Nickname: str
        :param _Mail: Creator's email address
        :type Mail: str
        :param _OrgType: Organization type
        :type OrgType: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._OrgId = None
        self._Nickname = None
        self._Mail = None
        self._OrgType = None
        self._RequestId = None

    @property
    def OrgId(self):
        return self._OrgId

    @OrgId.setter
    def OrgId(self, OrgId):
        self._OrgId = OrgId

    @property
    def Nickname(self):
        return self._Nickname

    @Nickname.setter
    def Nickname(self, Nickname):
        self._Nickname = Nickname

    @property
    def Mail(self):
        return self._Mail

    @Mail.setter
    def Mail(self, Mail):
        self._Mail = Mail

    @property
    def OrgType(self):
        return self._OrgType

    @OrgType.setter
    def OrgType(self, OrgType):
        self._OrgType = OrgType

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._OrgId = params.get("OrgId")
        self._Nickname = params.get("Nickname")
        self._Mail = params.get("Mail")
        self._OrgType = params.get("OrgType")
        self._RequestId = params.get("RequestId")


class DeleteOrganizationMemberFromNodeRequest(AbstractModel):
    """DeleteOrganizationMemberFromNode request structure.

    """

    def __init__(self):
        r"""
        :param _MemberUin: UIN of the member to be deleted
        :type MemberUin: int
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        """
        self._MemberUin = None
        self._NodeId = None

    @property
    def MemberUin(self):
        return self._MemberUin

    @MemberUin.setter
    def MemberUin(self, MemberUin):
        self._MemberUin = MemberUin

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId


    def _deserialize(self, params):
        self._MemberUin = params.get("MemberUin")
        self._NodeId = params.get("NodeId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteOrganizationMemberFromNodeResponse(AbstractModel):
    """DeleteOrganizationMemberFromNode response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteOrganizationMembersRequest(AbstractModel):
    """DeleteOrganizationMembers request structure.

    """

    def __init__(self):
        r"""
        :param _Uins: List of UINs of members to be deleted
        :type Uins: list of int non-negative
        """
        self._Uins = None

    @property
    def Uins(self):
        return self._Uins

    @Uins.setter
    def Uins(self, Uins):
        self._Uins = Uins


    def _deserialize(self, params):
        self._Uins = params.get("Uins")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteOrganizationMembersResponse(AbstractModel):
    """DeleteOrganizationMembers response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteOrganizationNodesRequest(AbstractModel):
    """DeleteOrganizationNodes request structure.

    """

    def __init__(self):
        r"""
        :param _NodeIds: Organizational unit ID list
        :type NodeIds: list of int non-negative
        """
        self._NodeIds = None

    @property
    def NodeIds(self):
        return self._NodeIds

    @NodeIds.setter
    def NodeIds(self, NodeIds):
        self._NodeIds = NodeIds


    def _deserialize(self, params):
        self._NodeIds = params.get("NodeIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteOrganizationNodesResponse(AbstractModel):
    """DeleteOrganizationNodes response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DeleteOrganizationRequest(AbstractModel):
    """DeleteOrganization request structure.

    """


class DeleteOrganizationResponse(AbstractModel):
    """DeleteOrganization response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class DenyOrganizationInvitationRequest(AbstractModel):
    """DenyOrganizationInvitation request structure.

    """

    def __init__(self):
        r"""
        :param _Id: Invitation ID
        :type Id: int
        """
        self._Id = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id


    def _deserialize(self, params):
        self._Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DenyOrganizationInvitationResponse(AbstractModel):
    """DenyOrganizationInvitation response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class GetOrganizationMemberRequest(AbstractModel):
    """GetOrganizationMember request structure.

    """

    def __init__(self):
        r"""
        :param _MemberUin: Organization member UIN
        :type MemberUin: int
        """
        self._MemberUin = None

    @property
    def MemberUin(self):
        return self._MemberUin

    @MemberUin.setter
    def MemberUin(self, MemberUin):
        self._MemberUin = MemberUin


    def _deserialize(self, params):
        self._MemberUin = params.get("MemberUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GetOrganizationMemberResponse(AbstractModel):
    """GetOrganizationMember response structure.

    """

    def __init__(self):
        r"""
        :param _Uin: Organization member UIN
        :type Uin: int
        :param _Name: Organization member name
        :type Name: str
        :param _Remark: Notes
        :type Remark: str
        :param _JoinTime: Joining time 
        :type JoinTime: str
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _NodeName: Organizational unit name
        :type NodeName: str
        :param _ParentNodeId: Parent organizational unit ID
        :type ParentNodeId: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._Uin = None
        self._Name = None
        self._Remark = None
        self._JoinTime = None
        self._NodeId = None
        self._NodeName = None
        self._ParentNodeId = None
        self._RequestId = None

    @property
    def Uin(self):
        return self._Uin

    @Uin.setter
    def Uin(self, Uin):
        self._Uin = Uin

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark

    @property
    def JoinTime(self):
        return self._JoinTime

    @JoinTime.setter
    def JoinTime(self, JoinTime):
        self._JoinTime = JoinTime

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def NodeName(self):
        return self._NodeName

    @NodeName.setter
    def NodeName(self, NodeName):
        self._NodeName = NodeName

    @property
    def ParentNodeId(self):
        return self._ParentNodeId

    @ParentNodeId.setter
    def ParentNodeId(self, ParentNodeId):
        self._ParentNodeId = ParentNodeId

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._Uin = params.get("Uin")
        self._Name = params.get("Name")
        self._Remark = params.get("Remark")
        self._JoinTime = params.get("JoinTime")
        self._NodeId = params.get("NodeId")
        self._NodeName = params.get("NodeName")
        self._ParentNodeId = params.get("ParentNodeId")
        self._RequestId = params.get("RequestId")


class GetOrganizationRequest(AbstractModel):
    """GetOrganization request structure.

    """


class GetOrganizationResponse(AbstractModel):
    """GetOrganization response structure.

    """

    def __init__(self):
        r"""
        :param _OrgId: Organization ID
        :type OrgId: int
        :param _HostUin: Creator UIN
        :type HostUin: int
        :param _Nickname: Creator's name
        :type Nickname: str
        :param _Mail: Creator's email address
        :type Mail: str
        :param _OrgType: Organization type
        :type OrgType: int
        :param _IsEmpty: Whether the organization is empty or not 
        :type IsEmpty: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._OrgId = None
        self._HostUin = None
        self._Nickname = None
        self._Mail = None
        self._OrgType = None
        self._IsEmpty = None
        self._RequestId = None

    @property
    def OrgId(self):
        return self._OrgId

    @OrgId.setter
    def OrgId(self, OrgId):
        self._OrgId = OrgId

    @property
    def HostUin(self):
        return self._HostUin

    @HostUin.setter
    def HostUin(self, HostUin):
        self._HostUin = HostUin

    @property
    def Nickname(self):
        return self._Nickname

    @Nickname.setter
    def Nickname(self, Nickname):
        self._Nickname = Nickname

    @property
    def Mail(self):
        return self._Mail

    @Mail.setter
    def Mail(self, Mail):
        self._Mail = Mail

    @property
    def OrgType(self):
        return self._OrgType

    @OrgType.setter
    def OrgType(self, OrgType):
        self._OrgType = OrgType

    @property
    def IsEmpty(self):
        return self._IsEmpty

    @IsEmpty.setter
    def IsEmpty(self, IsEmpty):
        self._IsEmpty = IsEmpty

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._OrgId = params.get("OrgId")
        self._HostUin = params.get("HostUin")
        self._Nickname = params.get("Nickname")
        self._Mail = params.get("Mail")
        self._OrgType = params.get("OrgType")
        self._IsEmpty = params.get("IsEmpty")
        self._RequestId = params.get("RequestId")


class ListOrganizationInvitationsRequest(AbstractModel):
    """ListOrganizationInvitations request structure.

    """

    def __init__(self):
        r"""
        :param _Invited: Whether to list the invitations you received or the invitations you sent. `1`: list the invitations you received; `0`: list the invitations you sent.
        :type Invited: int
        :param _Offset: Offset
        :type Offset: int
        :param _Limit: Limit
        :type Limit: int
        """
        self._Invited = None
        self._Offset = None
        self._Limit = None

    @property
    def Invited(self):
        return self._Invited

    @Invited.setter
    def Invited(self, Invited):
        self._Invited = Invited

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._Invited = params.get("Invited")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListOrganizationInvitationsResponse(AbstractModel):
    """ListOrganizationInvitations response structure.

    """

    def __init__(self):
        r"""
        :param _Invitations: List of invitations
        :type Invitations: list of OrgInvitation
        :param _TotalCount: Total number of results
        :type TotalCount: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._Invitations = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def Invitations(self):
        return self._Invitations

    @Invitations.setter
    def Invitations(self, Invitations):
        self._Invitations = Invitations

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Invitations") is not None:
            self._Invitations = []
            for item in params.get("Invitations"):
                obj = OrgInvitation()
                obj._deserialize(item)
                self._Invitations.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class ListOrganizationMembersRequest(AbstractModel):
    """ListOrganizationMembers request structure.

    """

    def __init__(self):
        r"""
        :param _Offset: Offset
        :type Offset: int
        :param _Limit: Limit
        :type Limit: int
        """
        self._Offset = None
        self._Limit = None

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListOrganizationMembersResponse(AbstractModel):
    """ListOrganizationMembers response structure.

    """

    def __init__(self):
        r"""
        :param _Members: Member list
        :type Members: list of OrgMember
        :param _TotalCount: Total number of results
        :type TotalCount: int
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._Members = None
        self._TotalCount = None
        self._RequestId = None

    @property
    def Members(self):
        return self._Members

    @Members.setter
    def Members(self, Members):
        self._Members = Members

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Members") is not None:
            self._Members = []
            for item in params.get("Members"):
                obj = OrgMember()
                obj._deserialize(item)
                self._Members.append(obj)
        self._TotalCount = params.get("TotalCount")
        self._RequestId = params.get("RequestId")


class ListOrganizationNodeMembersRequest(AbstractModel):
    """ListOrganizationNodeMembers request structure.

    """

    def __init__(self):
        r"""
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _Offset: Offset
        :type Offset: int
        :param _Limit: Limit
        :type Limit: int
        """
        self._NodeId = None
        self._Offset = None
        self._Limit = None

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def Offset(self):
        return self._Offset

    @Offset.setter
    def Offset(self, Offset):
        self._Offset = Offset

    @property
    def Limit(self):
        return self._Limit

    @Limit.setter
    def Limit(self, Limit):
        self._Limit = Limit


    def _deserialize(self, params):
        self._NodeId = params.get("NodeId")
        self._Offset = params.get("Offset")
        self._Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ListOrganizationNodeMembersResponse(AbstractModel):
    """ListOrganizationNodeMembers response structure.

    """

    def __init__(self):
        r"""
        :param _TotalCount: Total number of results
        :type TotalCount: int
        :param _Members: Member list
        :type Members: list of OrgMember
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._TotalCount = None
        self._Members = None
        self._RequestId = None

    @property
    def TotalCount(self):
        return self._TotalCount

    @TotalCount.setter
    def TotalCount(self, TotalCount):
        self._TotalCount = TotalCount

    @property
    def Members(self):
        return self._Members

    @Members.setter
    def Members(self, Members):
        self._Members = Members

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._TotalCount = params.get("TotalCount")
        if params.get("Members") is not None:
            self._Members = []
            for item in params.get("Members"):
                obj = OrgMember()
                obj._deserialize(item)
                self._Members.append(obj)
        self._RequestId = params.get("RequestId")


class ListOrganizationNodesRequest(AbstractModel):
    """ListOrganizationNodes request structure.

    """


class ListOrganizationNodesResponse(AbstractModel):
    """ListOrganizationNodes response structure.

    """

    def __init__(self):
        r"""
        :param _Nodes: Organizational unit list
        :type Nodes: list of OrgNode
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._Nodes = None
        self._RequestId = None

    @property
    def Nodes(self):
        return self._Nodes

    @Nodes.setter
    def Nodes(self, Nodes):
        self._Nodes = Nodes

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Nodes") is not None:
            self._Nodes = []
            for item in params.get("Nodes"):
                obj = OrgNode()
                obj._deserialize(item)
                self._Nodes.append(obj)
        self._RequestId = params.get("RequestId")


class MoveOrganizationMembersToNodeRequest(AbstractModel):
    """MoveOrganizationMembersToNode request structure.

    """

    def __init__(self):
        r"""
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _Uins: Member UIN list
        :type Uins: list of int non-negative
        """
        self._NodeId = None
        self._Uins = None

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def Uins(self):
        return self._Uins

    @Uins.setter
    def Uins(self, Uins):
        self._Uins = Uins


    def _deserialize(self, params):
        self._NodeId = params.get("NodeId")
        self._Uins = params.get("Uins")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MoveOrganizationMembersToNodeResponse(AbstractModel):
    """MoveOrganizationMembersToNode response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class OrgInvitation(AbstractModel):
    """Information on an invitation to an organization.

    """

    def __init__(self):
        r"""
        :param _Id: Invitation ID
        :type Id: int
        :param _Uin: UIN of the invitee
        :type Uin: int
        :param _HostUin: Creator UIN
        :type HostUin: int
        :param _HostName: Creator's name
        :type HostName: str
        :param _HostMail: Creator's email address
        :type HostMail: str
        :param _Status: Invitation status. `-1`: expired; `0`: normal; `1`: accepted; `2`: invalid; `3`: cancelled
        :type Status: int
        :param _Name: Name
        :type Name: str
        :param _Remark: Notes
        :type Remark: str
        :param _OrgType: Organization type
        :type OrgType: int
        :param _InviteTime: Time of invitation
        :type InviteTime: str
        :param _ExpireTime: Expiration time
        :type ExpireTime: str
        """
        self._Id = None
        self._Uin = None
        self._HostUin = None
        self._HostName = None
        self._HostMail = None
        self._Status = None
        self._Name = None
        self._Remark = None
        self._OrgType = None
        self._InviteTime = None
        self._ExpireTime = None

    @property
    def Id(self):
        return self._Id

    @Id.setter
    def Id(self, Id):
        self._Id = Id

    @property
    def Uin(self):
        return self._Uin

    @Uin.setter
    def Uin(self, Uin):
        self._Uin = Uin

    @property
    def HostUin(self):
        return self._HostUin

    @HostUin.setter
    def HostUin(self, HostUin):
        self._HostUin = HostUin

    @property
    def HostName(self):
        return self._HostName

    @HostName.setter
    def HostName(self, HostName):
        self._HostName = HostName

    @property
    def HostMail(self):
        return self._HostMail

    @HostMail.setter
    def HostMail(self, HostMail):
        self._HostMail = HostMail

    @property
    def Status(self):
        return self._Status

    @Status.setter
    def Status(self, Status):
        self._Status = Status

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark

    @property
    def OrgType(self):
        return self._OrgType

    @OrgType.setter
    def OrgType(self, OrgType):
        self._OrgType = OrgType

    @property
    def InviteTime(self):
        return self._InviteTime

    @InviteTime.setter
    def InviteTime(self, InviteTime):
        self._InviteTime = InviteTime

    @property
    def ExpireTime(self):
        return self._ExpireTime

    @ExpireTime.setter
    def ExpireTime(self, ExpireTime):
        self._ExpireTime = ExpireTime


    def _deserialize(self, params):
        self._Id = params.get("Id")
        self._Uin = params.get("Uin")
        self._HostUin = params.get("HostUin")
        self._HostName = params.get("HostName")
        self._HostMail = params.get("HostMail")
        self._Status = params.get("Status")
        self._Name = params.get("Name")
        self._Remark = params.get("Remark")
        self._OrgType = params.get("OrgType")
        self._InviteTime = params.get("InviteTime")
        self._ExpireTime = params.get("ExpireTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OrgMember(AbstractModel):
    """Information on an organization member.

    """

    def __init__(self):
        r"""
        :param _Uin: UIN
        :type Uin: int
        :param _Name: Name
        :type Name: str
        :param _Remark: Notes
        :type Remark: str
        :param _JoinTime: Joining time
        :type JoinTime: str
        """
        self._Uin = None
        self._Name = None
        self._Remark = None
        self._JoinTime = None

    @property
    def Uin(self):
        return self._Uin

    @Uin.setter
    def Uin(self, Uin):
        self._Uin = Uin

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark

    @property
    def JoinTime(self):
        return self._JoinTime

    @JoinTime.setter
    def JoinTime(self, JoinTime):
        self._JoinTime = JoinTime


    def _deserialize(self, params):
        self._Uin = params.get("Uin")
        self._Name = params.get("Name")
        self._Remark = params.get("Remark")
        self._JoinTime = params.get("JoinTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OrgNode(AbstractModel):
    """Information on an organizational unit.

    """

    def __init__(self):
        r"""
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _Name: Name
        :type Name: str
        :param _ParentNodeId: Parent organizational unit ID
        :type ParentNodeId: int
        :param _MemberCount: Number of members
        :type MemberCount: int
        """
        self._NodeId = None
        self._Name = None
        self._ParentNodeId = None
        self._MemberCount = None

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def ParentNodeId(self):
        return self._ParentNodeId

    @ParentNodeId.setter
    def ParentNodeId(self, ParentNodeId):
        self._ParentNodeId = ParentNodeId

    @property
    def MemberCount(self):
        return self._MemberCount

    @MemberCount.setter
    def MemberCount(self, MemberCount):
        self._MemberCount = MemberCount


    def _deserialize(self, params):
        self._NodeId = params.get("NodeId")
        self._Name = params.get("Name")
        self._ParentNodeId = params.get("ParentNodeId")
        self._MemberCount = params.get("MemberCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QuitOrganizationRequest(AbstractModel):
    """QuitOrganization request structure.

    """

    def __init__(self):
        r"""
        :param _OrgId: Organization ID
        :type OrgId: int
        """
        self._OrgId = None

    @property
    def OrgId(self):
        return self._OrgId

    @OrgId.setter
    def OrgId(self, OrgId):
        self._OrgId = OrgId


    def _deserialize(self, params):
        self._OrgId = params.get("OrgId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class QuitOrganizationResponse(AbstractModel):
    """QuitOrganization response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class SendOrganizationInvitationRequest(AbstractModel):
    """SendOrganizationInvitation request structure.

    """

    def __init__(self):
        r"""
        :param _InviteUin: UIN of the invitee
        :type InviteUin: int
        :param _Name: Name
        :type Name: str
        :param _Remark: Notes
        :type Remark: str
        """
        self._InviteUin = None
        self._Name = None
        self._Remark = None

    @property
    def InviteUin(self):
        return self._InviteUin

    @InviteUin.setter
    def InviteUin(self, InviteUin):
        self._InviteUin = InviteUin

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark


    def _deserialize(self, params):
        self._InviteUin = params.get("InviteUin")
        self._Name = params.get("Name")
        self._Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SendOrganizationInvitationResponse(AbstractModel):
    """SendOrganizationInvitation response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateOrganizationMemberRequest(AbstractModel):
    """UpdateOrganizationMember request structure.

    """

    def __init__(self):
        r"""
        :param _MemberUin: Member UIN
        :type MemberUin: int
        :param _Name: Name
        :type Name: str
        :param _Remark: Notes
        :type Remark: str
        """
        self._MemberUin = None
        self._Name = None
        self._Remark = None

    @property
    def MemberUin(self):
        return self._MemberUin

    @MemberUin.setter
    def MemberUin(self, MemberUin):
        self._MemberUin = MemberUin

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def Remark(self):
        return self._Remark

    @Remark.setter
    def Remark(self, Remark):
        self._Remark = Remark


    def _deserialize(self, params):
        self._MemberUin = params.get("MemberUin")
        self._Name = params.get("Name")
        self._Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateOrganizationMemberResponse(AbstractModel):
    """UpdateOrganizationMember response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")


class UpdateOrganizationNodeRequest(AbstractModel):
    """UpdateOrganizationNode request structure.

    """

    def __init__(self):
        r"""
        :param _NodeId: Organizational unit ID
        :type NodeId: int
        :param _Name: Name
        :type Name: str
        :param _ParentNodeId: Parent organizational unit ID
        :type ParentNodeId: int
        """
        self._NodeId = None
        self._Name = None
        self._ParentNodeId = None

    @property
    def NodeId(self):
        return self._NodeId

    @NodeId.setter
    def NodeId(self, NodeId):
        self._NodeId = NodeId

    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, Name):
        self._Name = Name

    @property
    def ParentNodeId(self):
        return self._ParentNodeId

    @ParentNodeId.setter
    def ParentNodeId(self, ParentNodeId):
        self._ParentNodeId = ParentNodeId


    def _deserialize(self, params):
        self._NodeId = params.get("NodeId")
        self._Name = params.get("Name")
        self._ParentNodeId = params.get("ParentNodeId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateOrganizationNodeResponse(AbstractModel):
    """UpdateOrganizationNode response structure.

    """

    def __init__(self):
        r"""
        :param _RequestId: The unique request ID, which is returned for each request. RequestId is required for locating a problem.
        :type RequestId: str
        """
        self._RequestId = None

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        self._RequestId = params.get("RequestId")