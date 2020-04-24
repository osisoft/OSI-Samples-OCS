import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { OidcService } from '../ocs-auth';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(public auth: OidcService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    request = request.clone({
      setHeaders: {
        Authorization: `${this.auth.userInfo.token_type} ${this.auth.userInfo.access_token}`,
      },
    });

    return next.handle(request);
  }
}
