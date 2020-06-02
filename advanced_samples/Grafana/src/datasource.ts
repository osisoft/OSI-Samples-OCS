import {
  DataQueryRequest,
  DataQueryResponse,
  DataSourceApi,
  DataSourceInstanceSettings,
  MutableDataFrame,
  FieldType,
} from '@grafana/data';

import { SdsQuery, SdsDataSourceOptions, SdsDataSourceType } from 'types';

export declare type BackendSrvRequest = {
  url: string;
  method?: string;
};

export interface BackendSrv {
  datasourceRequest(options: BackendSrvRequest): Promise<any>;
}

export class SdsDatasource extends DataSourceApi<SdsQuery, SdsDataSourceOptions> {
  name: string;
  proxyUrl: string;

  type: SdsDataSourceType;
  port: string;
  url: string;
  version: string;
  tenant: string;

  /** @ngInject */
  constructor(instanceSettings: DataSourceInstanceSettings<SdsDataSourceOptions>, private backendSrv: BackendSrv) {
    super(instanceSettings);
    this.name = instanceSettings.name;
    this.proxyUrl = instanceSettings.url ? instanceSettings.url.trim() : '';
    this.backendSrv = backendSrv;

    this.type = instanceSettings.jsonData?.type || SdsDataSourceType.OCS;
    this.port = instanceSettings.jsonData?.port || '5590';
    this.url = instanceSettings.jsonData?.url || '';
    this.version = instanceSettings.jsonData?.version || 'v1';
    this.tenant = instanceSettings.jsonData?.tenant || '';
  }

  async query(options: DataQueryRequest<SdsQuery>): Promise<DataQueryResponse> {
    const from = options.range?.from.utc().format();
    const to = options.range?.to.utc().format();
    const requests = options.targets.map(target => {
      const namespaceUrl =
        this.type === SdsDataSourceType.OCS
          ? `${this.proxyUrl}/ocs/api/${this.version}/tenants/${this.tenant}/namespaces/${target.namespace}`
          : `http://localhost:${this.port}/api/v1/tenants/default/namespaces/default`;
      return this.backendSrv.datasourceRequest({
        url: `${namespaceUrl}/streams/${target.stream}/data?startIndex=${from}&endIndex=${to}`,
        method: 'GET',
      });
    });

    const data = await Promise.all(requests).then(responses => {
      let i = 0;
      return responses.map(r => {
        const target = options.targets[i];
        i++;
        return new MutableDataFrame({
          refId: target.refId,
          name: target.stream,
          fields: Object.keys(r.data[0]).map(name => {
            const val0 = r.data[0][name];
            const date = Date.parse(val0);
            const num = Number(val0);
            const type =
              typeof val0 === 'string' && !isNaN(date)
                ? FieldType.time
                : val0 === true || val0 === false
                ? FieldType.boolean
                : !isNaN(num)
                ? FieldType.number
                : FieldType.string;
            return {
              name,
              values: r.data.map(d => (type === FieldType.time ? Date.parse(d[name]) : d[name])),
              type,
            };
          }),
        });
      });
    });

    return { data };
  }

  async testDatasource() {
    const url =
      this.type === SdsDataSourceType.OCS
        ? `${this.proxyUrl}/ocs/api/${this.version}/tenants/${this.tenant}/namespaces`
        : `http://localhost:${this.port}/api/v1/tenants/default/namespaces/default/streams`;
    return this.backendSrv
      .datasourceRequest({
        url,
        method: 'GET',
      })
      .then(r => {
        if (r.status === 200) {
          return {
            status: 'success',
            message: 'Data source is working',
          };
        } else {
          return {
            status: 'error',
            message: `${r.status}: ${r.statusText}`,
          };
        }
      });
  }

  getInterval(ms: number | undefined) {
    if (!ms) {
      // Default to every minute
      ms = 60000;
    }

    const date = new Date(ms);
    const hours = date
      .getUTCHours()
      .toString()
      .padStart(2, '0');
    const minutes = date
      .getUTCMinutes()
      .toString()
      .padStart(2, '0');
    const seconds = date
      .getSeconds()
      .toString()
      .padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
  }
}
