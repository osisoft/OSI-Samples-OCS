import { QueryEditorProps, SelectableValue } from '@grafana/data';
import { LegacyForms, InlineFormLabel } from '@grafana/ui';
import React, { PureComponent } from 'react';

import { SdsDataSource } from './DataSource';
import { SdsDataSourceOptions, SdsQuery } from './types';

const { AsyncSelect } = LegacyForms;

type Props = QueryEditorProps<SdsDataSource, SdsQuery, SdsDataSourceOptions>;

export class QueryEditor extends PureComponent<Props> {
  streams: SelectableValue<string>[] = [];

  constructor(props: Props) {
    super(props);
  }

  async queryStreamsAsync(value: string) {
    const { query } = this.props;
    query.stream = value;

    return await this.props.datasource.getStreams(value);
  }

  onSelectedStream = (value: SelectableValue<string>) => {
    const { onChange, query } = this.props;
    onChange({ ...query, stream: value.value || '' });
  };

  render() {
    const query = this.props.query;
    const { stream } = query;
    const select_stream: SelectableValue<string> = { label: stream, value: stream };

    return (
      <div className="gf-form">
        <InlineFormLabel width={8}>Stream</InlineFormLabel>
        <AsyncSelect
          defaultOptions={true}
          width={20}
          loadOptions={inputvalue => this.queryStreamsAsync(inputvalue)}
          defaultValue={stream}
          value={select_stream}
          onChange={inputvalue => this.onSelectedStream(inputvalue)}
          placeholder="Select Stream"
          loadingMessage={() => 'Loading streams...'}
          noOptionsMessage={() => 'No streams found'}
        />
        <LegacyForms.Input value={stream || ''} readOnly={true} hidden />
      </div>
    );
  }
}
