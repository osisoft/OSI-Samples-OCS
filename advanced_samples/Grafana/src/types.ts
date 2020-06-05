import { DataQuery, DataSourceJsonData } from '@grafana/data';

export enum SdsDataSourceType {
  OCS = 'ocs',
  EDS = 'eds',
}

export interface SdsQuery extends DataQuery {
  namespace: string;
  stream: string;
}

export interface SdsDataSourceOptions extends DataSourceJsonData {
  type: SdsDataSourceType;
  port: string;
  url: string;
  version: string;
  tenant: string;
  client: string;
}
