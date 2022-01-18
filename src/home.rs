use actix_web::{get, web, HttpRequest};
#[cfg(unix)]
use actix_web::{middleware, App, Error, HttpResponse, HttpServer};
use handlebars::Handlebars;

#[get("/")]
pub(crate) async fn process_home(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let body = hb.render("index", &data).unwrap();

    HttpResponse::Ok().body(body)
}