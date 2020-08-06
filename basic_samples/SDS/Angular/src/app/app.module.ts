import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { SdsRestService } from './sds/sds.rest.service';
import { DatasrcComponent } from './datasrc/datasrc.component';
import { routing, appRoutingProviders } from './app.routing';
import { OidcModule } from '../app/libraries/auth/ocs-auth';
import { AuthenticationGuard } from '../app/libraries/auth/extra/authguard';
import { AuthInterceptor } from '../app/libraries/auth/extra/authentication.interceptor';

@NgModule({
  declarations: [AppComponent, DatasrcComponent],
  imports: [BrowserModule, NgbModule, routing, OidcModule, HttpClientModule],
  providers: [
    appRoutingProviders,
    SdsRestService,
    AuthenticationGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
