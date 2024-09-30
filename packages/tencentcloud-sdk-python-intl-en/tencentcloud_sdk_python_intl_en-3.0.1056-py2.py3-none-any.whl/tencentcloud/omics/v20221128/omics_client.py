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

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.omics.v20221128 import models


class OmicsClient(AbstractClient):
    _apiVersion = '2022-11-28'
    _endpoint = 'omics.tencentcloudapi.com'
    _service = 'omics'


    def CreateEnvironment(self, request):
        """This API is used to create an environment for Tencent Healthcare Omics Platform.

        :param request: Request instance for CreateEnvironment.
        :type request: :class:`tencentcloud.omics.v20221128.models.CreateEnvironmentRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.CreateEnvironmentResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateEnvironment", params, headers=headers)
            response = json.loads(body)
            model = models.CreateEnvironmentResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def CreateVolume(self, request):
        """This API is used to create a volume.

        :param request: Request instance for CreateVolume.
        :type request: :class:`tencentcloud.omics.v20221128.models.CreateVolumeRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.CreateVolumeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateVolume", params, headers=headers)
            response = json.loads(body)
            model = models.CreateVolumeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteEnvironment(self, request):
        """This API is used to delete the environment.

        :param request: Request instance for DeleteEnvironment.
        :type request: :class:`tencentcloud.omics.v20221128.models.DeleteEnvironmentRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DeleteEnvironmentResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteEnvironment", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteEnvironmentResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteVolume(self, request):
        """This API is used to delete the volume.

        :param request: Request instance for DeleteVolume.
        :type request: :class:`tencentcloud.omics.v20221128.models.DeleteVolumeRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DeleteVolumeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteVolume", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteVolumeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DeleteVolumeData(self, request):
        """This API is used to delete the volume data.

        :param request: Request instance for DeleteVolumeData.
        :type request: :class:`tencentcloud.omics.v20221128.models.DeleteVolumeDataRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DeleteVolumeDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteVolumeData", params, headers=headers)
            response = json.loads(body)
            model = models.DeleteVolumeDataResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeEnvironments(self, request):
        """This API is used to query the environment list.

        :param request: Request instance for DescribeEnvironments.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeEnvironmentsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeEnvironmentsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEnvironments", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeEnvironmentsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeRunGroups(self, request):
        """This API is used to query the run group list.

        :param request: Request instance for DescribeRunGroups.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeRunGroupsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeRunGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeRunGroups", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRunGroupsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeRuns(self, request):
        """This API is used to query the run list.

        :param request: Request instance for DescribeRuns.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeRunsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeRunsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeRuns", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeRunsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTables(self, request):
        """This API is used to query the table.

        :param request: Request instance for DescribeTables.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeTablesRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeTablesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTables", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTablesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeTablesRows(self, request):
        """This API is used to query the table row data.

        :param request: Request instance for DescribeTablesRows.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeTablesRowsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeTablesRowsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTablesRows", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeTablesRowsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def DescribeVolumes(self, request):
        """This API is used to query the volume list.

        :param request: Request instance for DescribeVolumes.
        :type request: :class:`tencentcloud.omics.v20221128.models.DescribeVolumesRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.DescribeVolumesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeVolumes", params, headers=headers)
            response = json.loads(body)
            model = models.DescribeVolumesResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetRunCalls(self, request):
        """This API is used to query job details.

        :param request: Request instance for GetRunCalls.
        :type request: :class:`tencentcloud.omics.v20221128.models.GetRunCallsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.GetRunCallsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetRunCalls", params, headers=headers)
            response = json.loads(body)
            model = models.GetRunCallsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetRunMetadataFile(self, request):
        """This API is used to get the run details file.

        :param request: Request instance for GetRunMetadataFile.
        :type request: :class:`tencentcloud.omics.v20221128.models.GetRunMetadataFileRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.GetRunMetadataFileResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetRunMetadataFile", params, headers=headers)
            response = json.loads(body)
            model = models.GetRunMetadataFileResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def GetRunStatus(self, request):
        """This API is used to query run details.

        :param request: Request instance for GetRunStatus.
        :type request: :class:`tencentcloud.omics.v20221128.models.GetRunStatusRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.GetRunStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("GetRunStatus", params, headers=headers)
            response = json.loads(body)
            model = models.GetRunStatusResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ImportTableFile(self, request):
        """This API is used to import the table file.

        :param request: Request instance for ImportTableFile.
        :type request: :class:`tencentcloud.omics.v20221128.models.ImportTableFileRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.ImportTableFileResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ImportTableFile", params, headers=headers)
            response = json.loads(body)
            model = models.ImportTableFileResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def ModifyVolume(self, request):
        """This API is used to modify the volume.

        :param request: Request instance for ModifyVolume.
        :type request: :class:`tencentcloud.omics.v20221128.models.ModifyVolumeRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.ModifyVolumeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyVolume", params, headers=headers)
            response = json.loads(body)
            model = models.ModifyVolumeResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RetryRuns(self, request):
        """This API is used to retry the run.

        :param request: Request instance for RetryRuns.
        :type request: :class:`tencentcloud.omics.v20221128.models.RetryRunsRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.RetryRunsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RetryRuns", params, headers=headers)
            response = json.loads(body)
            model = models.RetryRunsResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RunApplication(self, request):
        """This API is used to run the application.

        :param request: Request instance for RunApplication.
        :type request: :class:`tencentcloud.omics.v20221128.models.RunApplicationRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.RunApplicationResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RunApplication", params, headers=headers)
            response = json.loads(body)
            model = models.RunApplicationResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def RunWorkflow(self, request):
        """This API is used to run the workflow.

        :param request: Request instance for RunWorkflow.
        :type request: :class:`tencentcloud.omics.v20221128.models.RunWorkflowRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.RunWorkflowResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RunWorkflow", params, headers=headers)
            response = json.loads(body)
            model = models.RunWorkflowResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))


    def TerminateRunGroup(self, request):
        """This API is used to terminate the run group.

        :param request: Request instance for TerminateRunGroup.
        :type request: :class:`tencentcloud.omics.v20221128.models.TerminateRunGroupRequest`
        :rtype: :class:`tencentcloud.omics.v20221128.models.TerminateRunGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("TerminateRunGroup", params, headers=headers)
            response = json.loads(body)
            model = models.TerminateRunGroupResponse()
            model._deserialize(response["Response"])
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))