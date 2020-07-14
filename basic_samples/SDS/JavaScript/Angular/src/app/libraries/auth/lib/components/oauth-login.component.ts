import { Component } from '@angular/core';
import { OidcService } from '../core/oidc.service';

@Component({
  selector: 'app-adal-login',
  template: '',
})
export class OAuthLoginComponent {
  constructor(private oidcService: OidcService) {
    this.oidcService.login();
  }
}
