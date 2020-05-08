import { DataQuery, DataSourceJsonData } from '@grafana/data';

export interface OcsQuery extends DataQuery {
  namespace: string;
  stream: string;
}

export interface OcsDataSourceOptions extends DataSourceJsonData {
  version: string;
  tenant: string;
  client: string;
}
