import { Component } from '@angular/core';
import { OidcService } from '../core/oidc.service';

@Component({
  selector: 'app-adal-logout',
  template: '',
})
export class OAuthLogoutComponent {
  constructor(private oidcService: OidcService) {
    this.oidcService.logout();
  }
}
