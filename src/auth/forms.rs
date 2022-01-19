use actix_web::{get, web, HttpRequest, post};
#[cfg(unix)]
use actix_web::{middleware, App, Error, HttpResponse, HttpServer};
use actix_web::http::{header};
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};
use crate::models::user::User;
use crate::schema::tusee_users::dsl::tusee_users;
use crate::utilities::utilities::establish_connection;
use diesel::prelude::*;
use crate::models::*;

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
        "error": false,
    });
    println!("it's in processing home");
    let body = hb.render("login", &data).unwrap();

    HttpResponse::Ok().body(body)
}

#[post("/login")]
pub(crate) async fn login_user(hb: web::Data<Handlebars<'_>>, info: web::Form<LoginInfo>) -> HttpResponse {
    use crate::schema::tusee_users::dsl::*;
    println!("=========={:?}=========", info);
    // validate against database
    let conn = establish_connection();
    tusee_users
        .select(password)
        .filter(email.eq(&info.username))
        .load::<User>(&conn);
    // if valid -> set jwt cookie
    // else -> render index page
    let data = json!({
        "error": true,
    });
    println!("it's in processing home");
    let body = hb.render("login", &data).unwrap();

    HttpResponse::Ok().body(body)
}
