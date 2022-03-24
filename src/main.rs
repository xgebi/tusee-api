#[macro_use]
extern crate actix_web;

#[macro_use]
extern crate serde_json;

#[macro_use]
extern crate diesel;

mod user;
mod services;
mod utilities;
mod models;
pub(crate) mod schema;
mod auth;
mod errors;
mod repositories;

use diesel::prelude::*;
use diesel::pg::PgConnection;
use std::env;
use std::ops::Deref;
use std::sync::{Arc, Mutex};
use actix_cors::Cors;

use actix_web::{get, post, web, http, App, HttpResponse, HttpServer, Responder};
use actix_web::http::header;
use diesel::dsl::all;
// use actix_cors::Cors;
use diesel::r2d2::{self, ConnectionManager};
use lettre::transport::smtp::authentication::Credentials;
use lettre::{Message, SmtpTransport, Transport};
use crate::user::user::{register_user, is_registration_enabled}; // log_user_in
use crate::auth::forms::{login_user, LoginInfo};
use serde::Deserialize;
use crate::utilities::configuration::Configuration;

#[derive(Debug, Deserialize)]
struct Config {
    database: String,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let config = Configuration::new();
    let manager = ConnectionManager::<PgConnection>::new(config.get_database());
    let pool = r2d2::Pool::builder()
        .build(manager)
        .expect("Failed to create pool.");
    let allowed_url = Arc::new(config.get_fe_url());
    HttpServer::new(move || {
        let cors = Cors::default()
            .allowed_origin(allowed_url.as_ref().as_str())
            .allowed_methods(vec!["OPTIONS", "GET", "POST", "PUT", "DELETE"])
            .allowed_headers(vec![header::AUTHORIZATION, header::ACCEPT])
            .allowed_header(header::CONTENT_TYPE)
            .max_age(3600);
        App::new()
            .wrap(cors)
            .app_data(pool.clone())
            .route("/login", web::post().to(auth::forms::login_user))
            .route("/register", web::post().to(auth::forms::process_registration))
            .route("/totp-setup", web::post().to(auth::forms::process_totp_setup))
            .service(
            web::resource("/people")
                .route(web::post().to(|person: web::Json<LoginInfo>| async {
                    HttpResponse::Ok()
                        .json(person)})
                    )
            )
    })
        .bind("127.0.0.1:8083")?
        .run()
        .await
}
