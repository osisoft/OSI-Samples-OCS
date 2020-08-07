import { DataSourcePlugin } from '@grafana/data';

import { ConfigEditor } from './ConfigEditor';
import { QueryEditor } from './QueryEditor';
import { SdsDataSource } from './DataSource';
import { SdsQuery, SdsDataSourceOptions, SdsDataSourceSecureOptions } from './types';

export const plugin = new DataSourcePlugin<SdsDataSource, SdsQuery, SdsDataSourceOptions, SdsDataSourceSecureOptions>(
  SdsDataSource
)
  .setConfigEditor(ConfigEditor)
  .setQueryEditor(QueryEditor);
