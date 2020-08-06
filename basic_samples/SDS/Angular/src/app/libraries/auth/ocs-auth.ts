import {
  NgModule,
  ModuleWithProviders,
  Optional,
  SkipSelf,
} from '@angular/core';
import { CommonModule } from '@angular/common';

import { OidcService } from './lib/core/oidc.service';
import { OAuthLoginComponent } from './lib/components/oauth-login.component';
import { OAuthLogoutComponent } from './lib/components/oauth-logout.component';
import { OAuthCallbackHandlerGuard } from './lib/core/oauth-callback-handler.guard';

@NgModule({
  imports: [CommonModule],
  declarations: [OAuthLoginComponent, OAuthLogoutComponent],
  providers: [OidcService, OAuthCallbackHandlerGuard],
})
export class OidcModule {
  static forRoot(): ModuleWithProviders<OidcModule> {
    return {
      ngModule: OidcModule,
      providers: [OidcService, OAuthCallbackHandlerGuard],
    };
  }

  constructor(@Optional() @SkipSelf() parentModule: OidcModule) {
    if (parentModule) {
      throw new Error(
        'OidcModule is already loaded. Import it in the AppModule only'
      );
    }
  }
}

export { OidcService } from './lib/core/oidc.service';
export { OAuthLoginComponent } from './lib/components/oauth-login.component';
export { OAuthLogoutComponent } from './lib/components/oauth-logout.component';
export { OAuthCallbackHandlerGuard } from './lib/core/oauth-callback-handler.guard';
