use actix_web::{get, web, HttpRequest, post};
#[cfg(unix)]
use actix_web::{middleware, App, Error, HttpResponse, HttpServer};
use actix_web::http::{header};
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Debug)]
pub struct LoginInfo {
    username: String,
    password: String,
}

#[get("/login")]
pub(crate) async fn show_login_page(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    // Check for jwt cookie
    // validate cookie
    // if cookie still valid -> redirect to dashboard
    // if invalid -> redirect to login
    // else render index page
    let data = json!({
        "name": "Handlebars"
    });
    println!("it's in processing home");
    let body = hb.render("login", &data).unwrap();

    HttpResponse::Ok().body(body)
}

#[post("/login")]
pub(crate) async fn login_user(info: web::Form<LoginInfo>) -> HttpResponse {
    println!("=========={:?}=========", info);
    // Check for jwt cookie
    // validate cookie
    // if cookie still valid -> redirect to dashboard
    // if invalid -> redirect to login
    // else render index page
    HttpResponse::Ok().finish()
}
