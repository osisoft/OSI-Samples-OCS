import json

from .BaseClient import BaseClient
from .DataView.DataView import DataView
from .DataView.DataItems import DataItems
from .DataView.FieldSets import FieldSets


class DataViews(object):
    """
    Client for interacting with Data Views
    """

    def __init__(self, client: BaseClient):
        """
        Initiliizes the Data View client
        :param client: This is the base client that is used to make the calls
        """
        self.__baseClient = client
        self.__setPathAndQueryTemplates()

    def postDataView(self, namespace_id, dataView):
        """Tells Sds Service to create a Data View based on local 'dataView'
            or get if existing Data View matches
        :param namespace_id: namespace to work against
        :param DataView: Data View definition.  Data View object expected
        :return: Retrieved Data View as Data View object
        """
        if namespace_id is None:
            raise TypeError
        if dataView is None or not isinstance(dataView, DataView):
            raise TypeError

        response = self.__baseClient.request(
            "post",
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView.Id,
            ),
            data=dataView.toJson()
        )

        self.__baseClient.checkResponse(
            response, f"Failed to create Data View, {dataView.Id}."
        )

        dataView = DataView.fromJson(response.json())
        return dataView

    def putDataView(self, namespace_id, dataView):
        """Tells Sds Service to update a Data View based on local 'dataView'
        :param namespace_id: namespace to work against
        :param dataView: Data View definition. Data View object expected
        :return: Retreived Data View as Data View object
        """
        if namespace_id is None:
            raise TypeError
        if dataView is None or not isinstance(dataView, DataView):
            raise TypeError

        response = self.__baseClient.request(
            "put",
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView.Id,
            ),
            data=dataView.toJson()
        )

        self.__baseClient.checkResponse(
            response, f"Failed to update Data View, {dataView.Id}."
        )

        return

    def deleteDataView(self, namespace_id, dataView_id):
        """
        Tells Sds Service to delete a Data View based on 'dataView_id'
        :param namespace_id: namespace to work against
        :param dataView_id:  id of Data View to delete
        """
        if namespace_id is None:
            raise TypeError
        if dataView_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "delete",
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            )
        )

        self.__baseClient.checkResponse(
            response, f"Failed to delete Data View, {dataView_id}."
        )

        return

    def getDataView(self, namespace_id, dataView_id):
        """
        Retrieves the Data View specified by 'dataView_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id:  id of Data View to get
        :return: Retreived Data View as Data View object
        """
        if namespace_id is None:
            raise TypeError
        if dataView_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "get",
            self.__dataViewPath.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
            )
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get Data View, {dataView_id}."
        )

        dataView = DataView.fromJson(response.json())
        return dataView

    def getDataViews(self, namespace_id, skip=0, count=100):
        """
        Retrieves all of the Data Views from Sds Service
        :param namespace_id: namespace to work against
        :param skip: Number of Data Views to skip
        :param count: Number of Data Views to return
        :return: array of Data Views
        """
        if namespace_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "get",
            self.__dataViewsPath.format(
                tenant_id=self.__baseClient.tenant, namespace_id=namespace_id
            ),
            params={"skip": skip, "count": count}
        )

        self.__baseClient.checkResponse(response, "Failed to get Data Views.")

        dataViews = json.loads(response.content)

        results = []
        for t in dataViews:
            results.append(DataView.fromJson(t))
        return results

    def getResolvedDataItems(
        self, namespace_id, dataView_id, query_id
    ):
        """
        Retrieves all of the resolved data items from the specified Data View from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: Data View to work against
        :param query_id: Query to see data items of
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "get",
            self.__dataViewResolvedDataItems.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                query_id=query_id,
            )
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedDataitems for Data View, {dataView_id}."
        )
        results = DataItems.fromJson(response.json())

        return results

    def getResolvedIneligibleDataItems(
        self, namespace_id, dataView_id, query_id
    ):
        """
        Retrieves all of the resolved ineligible data items from the specified Data View from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: Data View to work against
        :param query_id: Query to see data items of
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "get",
            self.__dataViewResolvedIneligibleDataItems.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id,
                query_id=query_id,
            )
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedIneligibleDataitems for Data View, {dataView_id}."
        )
        results = DataItems.fromJson(response.json())

        return results

    def getResolvedAvailableFieldSets(
        self, namespace_id, dataView_id
    ):
        """
        Retrieves all of the available field sets from the specified Data View from
            Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: Data View to work against
        :return:
        """
        if namespace_id is None:
            raise TypeError

        response = self.__baseClient.request(
            "get",
            self.__dataViewResolvedAvailableFieldSets.format(
                tenant_id=self.__baseClient.tenant,
                namespace_id=namespace_id,
                dataView_id=dataView_id
            )
        )

        self.__baseClient.checkResponse(
            response, f"Failed to get ResolvedAvailableFieldSetsfor Data View, {dataView_id}."
        )
        results = FieldSets.fromJson(response.json())

        return results

    def getDataInterpolated(
        self,
        namespace_id=None,
        dataView_id=None,
        count=None,
        form=None,
        startIndex=None,
        endIndex=None,
        interval=None,
        value_class=None,
        url=None
    ):
        """
        Retrieves the interpolated data of the 'dataView_id' from Sds Service
        :param namespace_id: namespace to work against
        :param dataView_id: Data View to work against
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
        if url is None:
            if namespace_id is None:
                raise TypeError
            if dataView_id is None:
                raise TypeError

        params = {
            "count": count,
            "form": form,
            "startIndex": startIndex,
            "endIndex": endIndex,
            "interval": interval
        }
        response = {}
        if url:
            response = self.__baseClient.request("get", url)
        else:
            response = self.__baseClient.request(
                "get",
                self.__dataViewDataInterpolated.format(
                    tenant_id=self.__baseClient.tenant,
                    namespace_id=namespace_id,
                    dataView_id=dataView_id,
                ),
                params=params
            )

        self.__baseClient.checkResponse(
            response,
            f"Failed to get Data View data interpolated for Data View, {dataView_id}.",
        )

        nextPage = None
        firstPage = None

        if "NextPage" in response.headers:
            nextPage = response.headers["NextPage"]

        if "FirstPage" in response.headers:
            firstPage = response.headers["FirstPage"]

        if form is not None:
            return response.text, nextPage, firstPage

        content = response.json()

        if value_class is None:
            return content, nextPage, firstPage
        return value_class.fromJson(content), nextPage, firstPage

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
        self.__dataViewResolvedDataItems = self.__dataViewResolved + \
            "/DataItems/{query_id}"
        self.__dataViewResolvedIneligibleDataItems = self.__dataViewResolved + \
            "/IneligibleDataItems/{query_id}"
        self.__dataViewResolvedAvailableFieldSets = self.__dataViewResolved + "/AvailableFieldSets"
        self.__dataViewData = self.__dataViewPath + "/data"
        self.__dataViewDataInterpolated = self.__dataViewData + "/interpolated"
