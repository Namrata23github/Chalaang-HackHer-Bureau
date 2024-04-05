import { Routes } from '@angular/router';
import { RegistrationLoginFormComponent } from './components/registration-login-form/registration-login-form.component';

export const routes: Routes = [

    {path: '**', component: RegistrationLoginFormComponent},
];
