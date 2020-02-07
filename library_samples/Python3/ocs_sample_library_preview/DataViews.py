import json

from .Dataview.DataView import DataView
from .Dataview.DataItems import DataItems
from .Dataview.FieldSets import FieldSets

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

    def getResolvedDataItems(
        self, namespace_id, dataView_id, query_id
    ):
        """
        Retrieves all of the DataGroups from the specified DataView from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param query_id: Query to see data items of
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataViewResolvedDataItems.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                query_id=query_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedDataitems for DataView, {dataView_id}."
        )
        results = DataItems.fromJson(response.json())

        return results
        
    def getResolvedIneligibleDataItems(
        self, namespace_id, dataView_id, query_id
    ):
        """
        Retrieves all of the DataGroups from the specified DataView from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param query_id: Query to see data items of
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataViewResolvedIneligibleDataItems.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                query_id=query_id,
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedIneligibleDataitems for DataView, {dataView_id}."
        )
        results = DataItems.fromJson(response.json())

        return results
         
    def getResolvedAvailableFieldSets(
        self, namespace_id, dataView_id,query_id
    ):
        """
        Retrieves all of the DataGroups from the specified DataView from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: DataView to work against
        :param query_id: Query to see data items of
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = requests.get(
            self.__dataViewResolvedAvailableFieldSets.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                query_id=query_id
            ),
            headers=self.__baseClient.sdsHeaders(),
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedAvailableFieldSetsfor DataView, {dataView_id}."
        )
        results = FieldSets.fromJson(response.json())

        return results

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
            self.__dataViewDataInterpolated.format(
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
        continuation_token = 1 # holder for the actual stuff
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
            self.__baseClient.uri_API + "-preview"
            "/Tenants/{tenant_id}/Namespaces/{namespace_id}"
        )

        self.__dataViewsPath = self.__basePath + "/dataviews"
        self.__dataViewPath = self.__dataViewsPath + "/{dataView_id}"
        self.__dataViewResolved = self.__dataViewPath + "/Resolved"
        self.__dataViewResolvedDataItems = self.__dataViewResolved + "/DataItems/{query_id}"
        self.__dataViewResolvedIneligibleDataItems = self.__dataViewResolved + "/IneligibleDataItems/{query_id}"
        self.__dataViewResolvedAvailableFieldSets =self.__dataViewResolved + "/AvailableFieldSets"
        self.__dataViewData = self.__dataViewPath + "/data"
        self.__dataViewDataInterpolated = self.__dataViewData + "/interpolated"
