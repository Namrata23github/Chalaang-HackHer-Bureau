import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrationLoginFormComponent } from './registration-login-form.component';

describe('RegistrationLoginFormComponent', () => {
  let component: RegistrationLoginFormComponent;
  let fixture: ComponentFixture<RegistrationLoginFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrationLoginFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RegistrationLoginFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
