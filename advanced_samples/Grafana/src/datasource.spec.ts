import { DataSourceInstanceSettings, MutableDataFrame, FieldType } from '@grafana/data';

import { SdsDatasource } from 'datasource';
import { SdsDataSourceOptions, SdsDataSourceType } from 'types';

describe('SdsDatasource', () => {
  const type = SdsDataSourceType.OCS;
  const port = 'PORT';
  const url = 'URL';
  const tenant = 'TENANT';
  const version = 'VERSION';
  const client = 'CLIENT';
  const settings: DataSourceInstanceSettings<SdsDataSourceOptions> = {
    id: 0,
    uid: '',
    name: '',
    type: '',
    meta: null as any,
    jsonData: {
      type,
      port,
      url,
      client,
      version,
      tenant,
    },
  };
  const edsSettings: DataSourceInstanceSettings<SdsDataSourceOptions> = {
    id: 0,
    uid: '',
    name: '',
    type: '',
    meta: null as any,
    jsonData: {
      type: SdsDataSourceType.EDS,
      port,
      url,
      client,
      version,
      tenant,
    },
  };
  const backendSrv = {
    datasourceRequest: () => new Promise(r => r),
  };

  describe('constructor', () => {
    it('should use passed in data source information', () => {
      const datasource = new SdsDatasource(settings, backendSrv as any);
      expect(datasource.type).toEqual(type);
      expect(datasource.port).toEqual(port);
      expect(datasource.url).toEqual(url);
      expect(datasource.version).toEqual(version);
      expect(datasource.tenant).toEqual(tenant);
    });
  });

  describe('query', () => {
    it('should query OCS with the expected parameters', done => {
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
      const datasource = new SdsDatasource(settings, backendSrv as any);
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

    it('should query EDS with the expected parameters', done => {
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
      const datasource = new SdsDatasource(edsSettings, backendSrv as any);
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
        url:
          'http://localhost:PORT/api/v1/tenants/default/namespaces/default/streams/STREAM/data?startIndex=FROM&endIndex=TO',
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

  describe('testDatasource', () => {
    it('should run a test query against OCS', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 200,
        })
      );
      const datasource = new SdsDatasource(settings, backendSrv as any);
      const response = datasource.testDatasource();
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: '/ocs/api/VERSION/tenants/TENANT/namespaces',
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

    it('should run a test query against EDS', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 200,
        })
      );
      const datasource = new SdsDatasource(edsSettings, backendSrv as any);
      const response = datasource.testDatasource();
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: 'http://localhost:PORT/api/v1/tenants/default/namespaces/default/streams',
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
      const datasource = new SdsDatasource(settings, backendSrv as any);
      const response = datasource.testDatasource();
      expect(backendSrv.datasourceRequest).toHaveBeenCalledWith({
        url: '/ocs/api/VERSION/tenants/TENANT/namespaces',
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

  describe('getInterval', () => {
    it('should parse ms into a time interval string', () => {
      const datasource = new SdsDatasource(settings, null as any);
      const response = datasource.getInterval(10000000);
      expect(response).toEqual('02:46:40');
    });
  });
});
