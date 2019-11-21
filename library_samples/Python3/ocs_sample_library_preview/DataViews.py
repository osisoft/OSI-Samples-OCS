import json

from .DataView.DataView import DataView
from .DataView.DataGroup import DataGroup

import requests


class DataViews(object):
    """
    Client for interacting with DataViews
    """

    def __init__(self, client):
        """
        Initiliizes the DataViews client
        :param client: This is the base client that is used to make the calls
        """
        self.__baseClient = client
        self.__setPathAndQueryTemplates()

    def postDataView(self, namespace_id, dataView):
        """Tells Sds Service to create a DataView based on local 'DataView'
            or get if existing DataView matches
        :param namespace_id: namespace to work against
        :param DataView: DataView definition.  DataView object expected
        :return: Retrieved DataView as DataView object
        """
        if namespace_id is None:
            raise TypeError
        if dataView is None or not isinstance(dataView, DataView):
            raise TypeError

        response = requests.post(
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView.Id,
            ),
            data=dataView.toJson(),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to create DataView, {dataView.Id}."
        )

        dataView = DataView.fromJson(response.json())
        return dataView

    def putDataView(self, namespace_id, dataView):
        """Tells Sds Service to update a DataView based on local 'dataView'
        :param namespace_id: namespace to work against
        :param dataView: DataView definition. DataView object expected
        :return: Retreived DataView as DataView object
        """
        if namespace_id is None:
            raise TypeError
        if dataView is None or not isinstance(dataView, DataView):
            raise TypeError
        response = requests.put(
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView.Id,
            ),
            data=dataView.toJson(),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to update DataView, {dataView.Id}."
        )

        return

    def deleteDataView(self, namespace_id, dataView_id):
        """
        Tells Sds Service to delete a DataView based on 'dataView_id'
        :param namespace_id: namespace to work against
        :param dataView_id:  id of DataView to delete
        """
        if namespace_id is None:
            raise TypeError
        if dataView_id is None:
            raise TypeError

        response = requests.delete(
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to delete DataView, {dataView_id}."
        )

        return

    def getDataView(self, namespace_id, dataView_id):
        """
        Retrieves the DataView specified by 'dataView_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id:  id of DataView to get
        :return: Retreived DataView as DataView object
        """
        if namespace_id is None:
            raise TypeError
        if dataView_id is None:
            raise TypeError

        response = requests.get(
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get DataView, {dataView_id}."
        )

        dataView = DataView.fromJson(response.json())
        return dataView

    def getDataViews(self, namespace_id, skip=0, count=100):
        """
        Retrieves all of the DataViews from Sds Service
        :param namespace_id: namespace to work against
        :param skip: Number of DataViews to skip
        :param count: Number of DataViews to return
        :return: array of DataViews
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataViewsPath.format(
                tenant_id=self.__baseClient.tenant, namespace_id=namespace_id
            ),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(response, "Failed to get DataViews.")

        dataViews = json.loads(response.content)

        results = []
        for t in dataViews:
            results.append(DataView.fromJson(t))
        return results

    def getDataGroups(
        self, namespace_id, dataView_id, skip=0, count=100, returnAsDynamicObject=False
    ):
        """
        Retrieves all of the DataGroups from the specified DataView from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param skip: Number of DataGroups to skip
        :param count: Number of DataGroups to return
        :param returnAsDynamicObject: returns the collection as dynamic object
                rather than a list of DataViews.  Added because the automated
                tests were failing.  Boolean
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataGroupPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            ),
            params={"skip": skip, "count": count},
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get DataGroups for DataView, {dataView_id}."
        )

        dataGroups = json.loads(response.content)

        if returnAsDynamicObject:
            return dataGroups

        results = []
        for dataGroup in dataGroups["DataGroups"]:
            results.append(DataGroup.fromJson(dataGroup))

        return results

    def getDataGroup(self, namespace_id, dataView_id, dataGroup_id):
        """
        Retrieves a DataGroup by 'dataGroup_id' from the specified
            DataView from Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param dataGroup_id: DataGroup to retrieve
        :return: the asked for DataGroup
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__getDataGroup.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                dataGroup_id=dataGroup_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response,
            f"Failed to get DataGroup, {dataGroup_id}," " for DataView, {dataView_id}.",
        )

        dataGroup = DataGroup.fromJson(response.json())
        return dataGroup

        # needs other parameters with smart

    def getDataInterpolated(
        self,
        namespace_id,
        dataView_id,
        count=None,
        form=None,
        continuationToken=None,
        startIndex=None,
        endIndex=None,
        interval=None,
        value_class=None,
    ):
        """
        Retrieves the interpolated data of the 'dataView_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param skip: number of values to skip
        :param count: number of values to return
        :param form: form definition
        :param startIndex: start index
        :param endIndex: end index
        :param interval: space between values
        :param value_class: Use this to auto format the data into the defined
            type.  The tpye is expected to have a fromJson method that takes a
            dynamicObject and converts it into the defined type.
          Otherwise you get a dynamic object
        :return:
        """
        if namespace_id is None:
            raise TypeError
        if dataView_id is None:
            raise TypeError

        params = {
            "count": count,
            "form": form,
            "continuationToken": continuationToken,
            "startIndex": startIndex,
            "endIndex": endIndex,
            "interval": interval,
        }
        response = requests.get(
            self.__getDataInterpolated.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
            params=params,
        )

        self.__baseClient.checkResponse(
            response,
            f"Failed to get DataView data interpolated for DataView, {dataView_id}.",
        )

        continuation_token = None
        next_page = response.headers.get("NextPage", None)
        if next_page:
            token_param = "&continuationToken="
            token_position = next_page.find(token_param)
            assert token_position > 0, "Could not find continuationToken in NextPage"
            end_position = next_page.find("&", token_position+1)
            end_position = None if end_position == -1 else end_position
            continuation_token = next_page[token_position +
                                           len(token_param):end_position]

        if form is not None:
            return response.text, continuation_token

        content = response.json()

        if value_class is None:
            return content, continuation_token
        return value_class.fromJson(content), continuation_token

    def __setPathAndQueryTemplates(self):
        """
        Internal  Sets the needed URLs
        :return:
        """
        self.__basePath = (
            self.__baseClient.uri_API +
            "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        )

        self.__dataViewsPath = self.__basePath + "/dataviews"
        self.__dataViewPath = self.__dataViewsPath + "/{dataView_id}"
        self.__dataGroupPath = self.__dataViewPath + "/datagroups"
        self.__getDataGroup = self.__dataGroupPath + "/{dataGroup_id}"
        self.__getDataInterpolated = self.__dataViewPath + "/data/interpolated"
