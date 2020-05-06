import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
} from '@angular/router';

import { OidcService } from '../core/oidc.service';

/**
 * This guard will run only when the user has successfully logged in and when adal tokens have been renewed. On login this logic will
 * occur in the window that the app is being run in. On token renewal this logic will occur in a hidden iframe.
 */
@Injectable()
export class OAuthCallbackHandlerGuard implements CanActivate {
  constructor(private router: Router, private oidcService: OidcService) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Promise<boolean> {
    this.oidcService.windowCallbackInProgress = true;
    const signinCallback = window.frameElement
      ? this.oidcService.handleSilentCallback()
      : this.oidcService.handleRedirectCallback();

    return signinCallback
      .then(() => {
        this.oidcService.emitLoginSuccessEvent(true);
        this.oidcService.windowCallbackInProgress = false;
        this.router.navigate([]);
        return true;
      })
      .catch(() => {
        this.oidcService.emitLoginSuccessEvent(false);
        this.oidcService.windowCallbackInProgress = false;
        this.router.navigate(['login']);
        return false;
      });
  }
}
