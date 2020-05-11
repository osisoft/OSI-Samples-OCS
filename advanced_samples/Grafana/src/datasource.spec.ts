import { DataSourceInstanceSettings, MutableDataFrame, FieldType } from '@grafana/data';

import { OcsDatasource } from 'datasource';
import { OcsDataSourceOptions } from 'types';

describe('OcsDatasource', () => {
  const tenant = 'TENANT';
  const version = 'VERSION';
  const settings: DataSourceInstanceSettings<OcsDataSourceOptions> = {
    id: 0,
    name: '',
    type: '',
    meta: null as any,
    jsonData: {
      client: 'client',
      version: version,
      tenant: tenant,
    },
  };
  const backendSrv = {
    datasourceRequest: () => new Promise(r => r),
  };

  describe('constructor', () => {
    it('should use passed in version/tenant information', () => {
      const datasource = new OcsDatasource(settings, backendSrv as any);
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
      const datasource = new OcsDatasource(settings, backendSrv as any);
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

  describe('testDatasource', () => {
    it('should run a test query', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 200,
        })
      );
      const datasource = new OcsDatasource(settings, backendSrv as any);
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

    it('should handle test failure', done => {
      spyOn(backendSrv, 'datasourceRequest').and.returnValue(
        Promise.resolve({
          status: 400,
          statusText: 'Error',
        })
      );
      const datasource = new OcsDatasource(settings, backendSrv as any);
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
      const datasource = new OcsDatasource(settings, null as any);
      const response = datasource.getInterval(10000000);
      expect(response).toEqual('02:46:40');
    });
  });
});
