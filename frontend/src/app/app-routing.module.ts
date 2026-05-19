
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from './core/guards/auth.guard';
import { ArticulosComponent } from './paginas/articulos/articulos.component';
import { CatalogoComponent } from './paginas/catalogo/catalogo.component';
import { IntercambiosComponent } from './paginas/intercambios/intercambios.component';
import { LoginComponent } from './paginas/login/login.component';
import { PerfilComponent } from './paginas/perfil/perfil.component';
import { RegistroComponent } from './paginas/registro/registro.component';

const routes: Routes = [
  { path: '', redirectTo: 'catalogo', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'registro', component: RegistroComponent },
  { path: 'catalogo', component: CatalogoComponent },
  { path: 'perfil', component: PerfilComponent, canActivate: [AuthGuard] },
  { path: 'articulos', component: ArticulosComponent, canActivate: [AuthGuard] },
  {
    path: 'intercambios',
    component: IntercambiosComponent,
    canActivate: [AuthGuard],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
