import {
  DataQueryRequest,
  DataQueryResponse,
  DataSourceApi,
  DataSourceInstanceSettings,
  MutableDataFrame,
  FieldType,
  SelectableValue,
} from '@grafana/data';

import { SdsQuery, SdsDataSourceOptions, SdsDataSourceType } from 'types';

export declare type BackendSrvRequest = {
  url: string;
  method?: string;
};

export interface BackendSrv {
  datasourceRequest(options: BackendSrvRequest): Promise<any>;
}

export class SdsDataSource extends DataSourceApi<SdsQuery, SdsDataSourceOptions> {
  name: string;
  proxyUrl: string;

  type: SdsDataSourceType;
  eds_port: string;
  ocs_url: string;
  ocs_version: string;
  ocs_tenant: string;
  oauthPassThru: boolean;
  namespace: string;

  get streamsUrl() {
    return this.type === SdsDataSourceType.OCS
      ? `${this.proxyUrl}/ocs/api/${this.ocs_version}/tenants/${this.ocs_tenant}/namespaces/${this.namespace}/streams`
      : `http://localhost:${this.eds_port}/api/v1/tenants/default/namespaces/${this.namespace}/streams`;
  }

  /** @ngInject */
  constructor(instanceSettings: DataSourceInstanceSettings<SdsDataSourceOptions>, private backendSrv: BackendSrv) {
    super(instanceSettings);
    this.name = instanceSettings.name;
    this.proxyUrl = instanceSettings.url ? instanceSettings.url.trim() : '';
    this.backendSrv = backendSrv;

    this.type = instanceSettings.jsonData?.type || SdsDataSourceType.OCS;
    this.eds_port = instanceSettings.jsonData?.eds_port || '5590';
    this.ocs_url = instanceSettings.jsonData?.ocs_url || '';
    this.ocs_version = instanceSettings.jsonData?.ocs_version || 'v1';
    this.ocs_tenant = instanceSettings.jsonData?.ocs_tenant || '';
    this.oauthPassThru = instanceSettings.jsonData?.oauthPassThru || false;
    this.namespace = instanceSettings.jsonData.namespace || '';
  }

  async query(options: DataQueryRequest<SdsQuery>): Promise<DataQueryResponse> {
    const from = options.range?.from.utc().format();
    const to = options.range?.to.utc().format();
    const requests = options.targets.map(target => {
      if (!target.stream) {
        return new Promise(resolve => resolve(null));
      }
      return this.backendSrv.datasourceRequest({
        url: `${this.streamsUrl}/${target.stream}/data?startIndex=${from}&endIndex=${to}`,
        method: 'GET',
      });
    });

    const data = await Promise.all(requests).then(responses => {
      let i = 0;
      return responses.map((r: any) => {
        if (!r) {
          return new MutableDataFrame();
        }

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

  async getStreams(query: string): Promise<SelectableValue<string>[]> {
    if (this.namespace) {
      const url = query ? `${this.streamsUrl}?query=*${query}*` : this.streamsUrl;
      const requests = this.backendSrv.datasourceRequest({ url, method: 'GET' });
      return await Promise.resolve(requests).then(responses =>
        Object.keys(responses.data).map(r => ({ value: responses.data[r].Id, label: responses.data[r].Id }))
      );
    } else {
      return await new Promise(resolve => resolve([]));
    }
  }

  async testDatasource() {
    return this.backendSrv
      .datasourceRequest({
        url: this.streamsUrl,
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
}
