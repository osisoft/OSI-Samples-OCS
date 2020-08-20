import { DataSourceInstanceSettings, MutableDataFrame, FieldType } from '@grafana/data';

import { SdsDataSource } from 'DataSource';
import { SdsDataSourceOptions, SdsDataSourceType } from 'types';

describe('SdsDataSource', () => {
  const eds_port = 'PORT';
  const ocs_url = 'URL';
  const ocs_version = 'VERSION';
  const ocs_tenant = 'TENANT';
  const ocs_client = 'CLIENT';
  const oauthPassThru = false;
  const namespace = 'NAMESPACE';
  const ocsSettings: DataSourceInstanceSettings<SdsDataSourceOptions> = {
    id: 0,
    uid: '',
    name: '',
    type: '',
    meta: null as any,
    jsonData: {
      type: SdsDataSourceType.OCS,
      eds_port,
      ocs_url,
      ocs_version,
      ocs_tenant,
      ocs_client,
      oauthPassThru,
      namespace,
    },
  };
  const edsSettings = { ...ocsSettings, ...{ jsonData: { ...ocsSettings.jsonData, type: SdsDataSourceType.EDS } } };
  const backendSrv = {
    datasourceRequest: () => new Promise(r => r),
  };

  describe('constructor', () => {
    it('should use passed in data source information', () => {
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      expect(datasource.type).toEqual(SdsDataSourceType.OCS);
      expect(datasource.eds_port).toEqual(eds_port);
      expect(datasource.ocs_url).toEqual(ocs_url);
      expect(datasource.ocs_version).toEqual(ocs_version);
      expect(datasource.ocs_tenant).toEqual(ocs_tenant);
      expect(datasource.oauthPassThru).toEqual(oauthPassThru);
      expect(datasource.namespace).toEqual(namespace);
    });
  });

  describe('getStreamsUrl', () => {
    it('should return the correct URL for OCS', () => {
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      expect(datasource.streamsUrl).toEqual('/ocs/api/VERSION/tenants/TENANT/namespaces/NAMESPACE/streams');
    });

    it('should return the correct URL for EDS', () => {
      const datasource = new SdsDataSource(edsSettings, backendSrv as any);
      expect(datasource.streamsUrl).toEqual(
        'http://localhost:PORT/api/v1/tenants/default/namespaces/NAMESPACE/streams'
      );
    });
  });

  describe('query', () => {
    it('should query with the expected parameters', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          data: [
            {
              TimeStamp: '2020-01-01',
              Boolean: true,
              Number: 1,
              String: 'A',
            },
          ],
        })
      );
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      const options = {
        range: {
          from: {
            utc: () => ({
              format: () => 'FROM',
            }),
          },
          to: {
            utc: () => ({
              format: () => 'TO',
            }),
          },
        },
        targets: [
          {
            refId: 'REFID',
            namespace: 'NAMESPACE',
            stream: 'STREAM',
          },
        ],
      };
      const response = datasource.query(options as any);
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: '/ocs/api/VERSION/tenants/TENANT/namespaces/NAMESPACE/streams/STREAM/data?startIndex=FROM&endIndex=TO',
        method: 'GET',
      });
      response.then(r => {
        expect(JSON.stringify(r)).toEqual(
          JSON.stringify({
            data: [
              new MutableDataFrame({
                refId: 'REFID',
                name: 'STREAM',
                fields: [
                  {
                    name: 'TimeStamp',
                    type: FieldType.time,
                    values: [Date.parse('2020-01-01')],
                  },
                  {
                    name: 'Boolean',
                    type: FieldType.boolean,
                    values: [true],
                  },
                  {
                    name: 'Number',
                    type: FieldType.number,
                    values: [1],
                  },
                  {
                    name: 'String',
                    type: FieldType.string,
                    values: ['A'],
                  },
                ],
              }),
            ],
          })
        );
        done();
      });
    });
  });

  describe('getStreams', () => {
    it('should return empty if namespace is not defined', done => {
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      datasource.namespace = '';
      const result = datasource.getStreams('');
      result.then(r => {
        expect(r).toEqual([]);
        done();
      });
    });

    it('should query for streams', done => {
      const Id = 'Stream';
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(Promise.resolve({ data: [{ Id }] }));
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      const result = datasource.getStreams('test');
      result.then(r => {
        expect(r).toEqual([{ value: Id, label: Id }]);
        done();
      });
    });
  });

  describe('testDatasource', () => {
    it('should run a test query', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 200,
        })
      );
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      const response = datasource.testDatasource();
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: '/ocs/api/VERSION/tenants/TENANT/namespaces/NAMESPACE/streams',
        method: 'GET',
      });
      response.then(r => {
        expect(r).toEqual({
          status: 'success',
          message: 'Data source is working',
        });
        done();
      });
    });

    it('should handle test failure', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 400,
          statusText: 'Error',
        })
      );
      const datasource = new SdsDataSource(ocsSettings, backendSrv as any);
      const response = datasource.testDatasource();
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: '/ocs/api/VERSION/tenants/TENANT/namespaces/NAMESPACE/streams',
        method: 'GET',
      });
      response.then(r => {
        expect(r).toEqual({
          status: 'error',
          message: '400: Error',
        });
        done();
      });
    });
  });
});
