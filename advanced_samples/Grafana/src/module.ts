import { QueryCtrl } from 'grafana/app/plugins/sdk';

import { SdsDatasource } from './datasource';
import { SdsDataSourceType } from './types';

export class SdsConfigCtrl {
  static templateUrl = 'partials/config.html';

  /** @ngInject */
  constructor($scope) {
    if (!$scope.ctrl.current.jsonData.type) {
      $scope.ctrl.current.jsonData.type = SdsDataSourceType.OCS;
    }
  }
}

export class SdsQueryCtrl extends QueryCtrl {
  static templateUrl = 'partials/query.editor.html';
}

export { SdsDatasource as Datasource, SdsQueryCtrl as QueryCtrl, SdsConfigCtrl as ConfigCtrl };
