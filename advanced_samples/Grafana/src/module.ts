import { QueryCtrl } from 'grafana/app/plugins/sdk';

import { OcsDatasource } from './datasource';

export class OcsConfigCtrl {
  static templateUrl = 'partials/config.html';
}

export class OcsQueryCtrl extends QueryCtrl {
  static templateUrl = 'partials/query.editor.html';
}

export { OcsDatasource as Datasource, OcsQueryCtrl as QueryCtrl, OcsConfigCtrl as ConfigCtrl };
