import { Component, OnInit } from '@angular/core';
import { UserManagerSettings, WebStorageStateStore } from 'oidc-client';

import { OidcService } from './libraries/auth/ocs-auth';
import { SdsConfig } from './config/sdsconfig.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [],
})
export class AppComponent implements OnInit {
  private sdsConfig: SdsConfig;
  private authConfig: UserManagerSettings;

  constructor(private auth: OidcService) {
    const sdsConfig = './config/sdsconfig.json';
    import(sdsConfig).then((data) => {
      this.sdsConfig = data as SdsConfig;
    });
  }

  ngOnInit(): void {
    const oidcConfig = './config/oidc.config.json';
    import(oidcConfig).then((data) => {
      const configFromJson = data as UserManagerSettings;
      this.authConfig = {
        ...configFromJson,
        userStore: new WebStorageStateStore({ store: window.localStorage }),
        acr_values: `tenant:${this.sdsConfig.tenantId}`,
        response_type: 'code',
        scope: 'openid ocsapi',
        filterProtocolClaims: true,
        loadUserInfo: true,
        revokeAccessTokenOnSignout: true,
        automaticSilentRenew: true,
        accessTokenExpiringNotificationTime: 60,
        silentRequestTimeout: 10000,
      };

      this.auth.init(this.authConfig);
    });
  }

  get loggedIn() {
    return this.auth.userInfo !== null;
  }

  login() {
    this.auth.login();
  }

  logout() {
    this.auth.logout();
  }
}
