import {
  DataSourcePluginOptionsEditorProps,
  onUpdateDatasourceSecureJsonDataOption,
  onUpdateDatasourceJsonDataOption,
  onUpdateDatasourceJsonDataOptionChecked,
  onUpdateDatasourceJsonDataOptionSelect,
} from '@grafana/data';
import { LegacyForms, InlineFormLabel } from '@grafana/ui';
import React, { PureComponent, SyntheticEvent } from 'react';

import { SdsDataSourceOptions, SdsDataSourceType, SdsDataSourceSecureOptions } from './types';

const { FormField, Select, SecretFormField, Switch } = LegacyForms;

interface Props extends DataSourcePluginOptionsEditorProps<SdsDataSourceOptions, SdsDataSourceSecureOptions> {}

export class ConfigEditor extends PureComponent<Props> {
  typeLabels = {
    [SdsDataSourceType.OCS]: 'OSIsoft Cloud Services',
    [SdsDataSourceType.EDS]: 'Edge Data Store',
  };

  typeOptions = [
    { value: SdsDataSourceType.OCS, label: this.typeLabels[SdsDataSourceType.OCS] },
    { value: SdsDataSourceType.EDS, label: this.typeLabels[SdsDataSourceType.EDS] },
  ];

  edsNamespaceOptions = [
    { value: 'default', label: 'default' },
    { value: 'diagnostics', label: 'diagnostics' },
  ];

  warningStyle = {
    color: 'orange',
    alignSelf: 'center',
  };

  onResetClientSecret = (event: SyntheticEvent) => {
    event.preventDefault();
    const { onOptionsChange, options } = this.props;
    const secureJsonData = {
      ...options.secureJsonData,
      ocs_secret: '',
    };
    const secureJsonFields = {
      ...options.secureJsonFields,
      ocs_secret: false,
    };
    onOptionsChange({ ...options, secureJsonData, secureJsonFields });
  };

  render() {
    const { options } = this.props;
    const { jsonData, secureJsonFields, secureJsonData } = options;

    // Fill in defaults
    if (!jsonData.type) {
      jsonData.type = SdsDataSourceType.OCS;
    }
    if (!jsonData.eds_port) {
      jsonData.eds_port = '5590';
    }
    if (!jsonData.ocs_url) {
      jsonData.ocs_url = 'https://dat-b.osisoft.com';
    }
    if (!jsonData.ocs_version) {
      jsonData.ocs_version = 'v1';
    }
    if (jsonData.oauthPassThru == null) {
      jsonData.oauthPassThru = false;
    }
    if (jsonData.type == SdsDataSourceType.EDS && !jsonData.namespace) {
      jsonData.namespace = 'default';
    }

    return (
      <div>
        <div className="gf-form-group">
          <h3 className="page-heading">Sequential Data Store</h3>
          <div className="gf-form">
            <InlineFormLabel
              width={10}
              tooltip="The type of SDS source system in use, either OSIsoft Cloud Services or Edge Data Store"
            >
              Type
            </InlineFormLabel>
            <Select
              width={20}
              placeholder="Select type of source system..."
              options={this.typeOptions}
              onChange={onUpdateDatasourceJsonDataOptionSelect(this.props, 'type')}
              value={{ value: jsonData.type, label: this.typeLabels[jsonData.type] }}
            />
          </div>
        </div>
        {jsonData.type === SdsDataSourceType.EDS ? (
          <div className="gf-form-group">
            <h3 className="page-heading">Edge Data Store</h3>
            <div className="gf-form">
              <FormField
                required={true}
                label="Port"
                tooltip="The port number used by Edge Data Store"
                placeholder="5590"
                labelWidth={10}
                inputWidth={20}
                onChange={onUpdateDatasourceJsonDataOption(this.props, 'eds_port')}
                value={jsonData.eds_port || ''}
              />
            </div>
            <div className="gf-form">
              <InlineFormLabel width={10} tooltip="The Namespace in your for OSIsoft Cloud Services tenant">
                Namespace
              </InlineFormLabel>
              <Select
                width={20}
                placeholder="EDS Namespace"
                options={this.edsNamespaceOptions}
                onChange={onUpdateDatasourceJsonDataOptionSelect(this.props, 'namespace')}
                value={{ value: jsonData.namespace, label: jsonData.namespace }}
              />
            </div>
          </div>
        ) : (
          <div className="gf-form-group">
            <h3 className="page-heading">OSIsoft Cloud Services</h3>
            <div className="gf-form">
              <FormField
                required={true}
                label="URL"
                tooltip="The URL for OSIsoft Cloud Services"
                placeholder="https://dat-b.osisoft.com"
                labelWidth={10}
                inputWidth={20}
                onChange={onUpdateDatasourceJsonDataOption(this.props, 'ocs_url')}
                value={jsonData.ocs_url || ''}
              />
            </div>
            <div className="gf-form">
              <FormField
                required={true}
                label="API Version"
                tooltip="The version of the OCS API to use"
                placeholder="v1"
                labelWidth={10}
                inputWidth={20}
                onChange={onUpdateDatasourceJsonDataOption(this.props, 'ocs_version')}
                value={jsonData.ocs_version || ''}
              />
            </div>
            <div className="gf-form">
              <FormField
                required={true}
                label="Tenant ID"
                tooltip="The ID of your OSIsoft Cloud Services tenant"
                placeholder="00000000-0000-0000-0000-000000000000"
                labelWidth={10}
                inputWidth={20}
                onChange={onUpdateDatasourceJsonDataOption(this.props, 'ocs_tenant')}
                value={jsonData.ocs_tenant || ''}
              />
            </div>
            <div className="gf-form">
              <FormField
                required={true}
                label="Namespace"
                tooltip="The Namespace in your for OSIsoft Cloud Services tenant"
                placeholder="Enter a Namespace ID..."
                labelWidth={10}
                inputWidth={20}
                onChange={onUpdateDatasourceJsonDataOption(this.props, 'namespace')}
                value={jsonData.namespace || ''}
              />
            </div>
            <div className="gf-form-inline">
              <Switch
                label="Use OAuth token"
                labelClass="width-10"
                tooltip="Whether to use Grafana login OAuth token against OSIsoft Cloud Services API"
                onChange={onUpdateDatasourceJsonDataOptionChecked(this.props, 'oauthPassThru')}
                checked={jsonData.oauthPassThru}
              />
              {jsonData.oauthPassThru && (
                <div style={this.warningStyle}>
                  Warning: Requires modified Grafana server, see{' '}
                  <a href="https://github.com/grafana/grafana/issues/26350">this issue</a>
                </div>
              )}
            </div>
            {!jsonData.oauthPassThru && (
              <div className="gf-form">
                <FormField
                  label="Client ID"
                  tooltip="The ID of the Client Credentials client to authenticate against your OCS tenant"
                  placeholder="00000000-0000-0000-0000-000000000000"
                  labelWidth={10}
                  inputWidth={20}
                  onChange={onUpdateDatasourceJsonDataOption(this.props, 'ocs_client')}
                  value={jsonData.ocs_client || ''}
                />
              </div>
            )}
            {!jsonData.oauthPassThru && (
              <div className="gf-form">
                <SecretFormField
                  required={true}
                  label="Client Secret"
                  tooltip="The secret for the specified Client Credentials client"
                  type="password"
                  placeholder="Enter a Client secret..."
                  labelWidth={10}
                  inputWidth={20}
                  onChange={onUpdateDatasourceSecureJsonDataOption(this.props, 'ocs_secret')}
                  onReset={this.onResetClientSecret}
                  isConfigured={secureJsonFields?.ocs_secret || false}
                  value={secureJsonData?.ocs_secret || ''}
                />
              </div>
            )}
          </div>
        )}
      </div>
    );
  }
}
