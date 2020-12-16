import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DatasrcComponent } from './datasrc.component';

describe('DatasrcComponent', () => {
  let component: DatasrcComponent;
  let fixture: ComponentFixture<DatasrcComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [DatasrcComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatasrcComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
