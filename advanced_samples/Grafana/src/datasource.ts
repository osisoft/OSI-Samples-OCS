import { DataQueryRequest, DataQueryResponse, DataSourceApi, DataSourceInstanceSettings, MutableDataFrame, FieldType } from '@grafana/data';
import { BackendSrv } from '@grafana/runtime';

import { OcsQuery, OcsDataSourceOptions } from 'types';

export class OcsDatasource extends DataSourceApi<OcsQuery, OcsDataSourceOptions> {
  type: string;
  name: string;
  url: string;

  version: string;
  tenant: string;

  /** @ngInject */
  constructor(instanceSettings: DataSourceInstanceSettings<OcsDataSourceOptions>, private backendSrv: BackendSrv) {
    super(instanceSettings);
    this.type = instanceSettings.type;
    this.name = instanceSettings.name;
    this.url = instanceSettings.url ? instanceSettings.url.trim() : '';
    this.backendSrv = backendSrv;

    this.version = instanceSettings.jsonData?.version || 'v1';
    this.tenant = instanceSettings.jsonData?.tenant || '';
  }

  async query(options: DataQueryRequest<OcsQuery>): Promise<DataQueryResponse> {
    const from = options.range?.from.utc().format();
    const to = options.range?.to.utc().format();
    const requests = options.targets.map(target => {
      return this.backendSrv.datasourceRequest({
        url: `${this.url}/ocs/api/${this.version}/tenants/${this.tenant}/namespaces/${target.namespace}/streams/${target.stream}/data?startIndex=${from}&endIndex=${to}`,
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
    return this.backendSrv
      .datasourceRequest({
        url: `${this.url}/ocs/api/${this.version}/tenants/${this.tenant}/namespaces`,
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
