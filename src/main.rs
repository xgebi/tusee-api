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

use actix_web::{get, post, web, http, App, HttpResponse, HttpServer, Responder};
// use actix_cors::Cors;
use diesel::r2d2::{self, ConnectionManager};
use lettre::transport::smtp::authentication::Credentials;
use lettre::{Message, SmtpTransport, Transport};
use handlebars::Handlebars;
use crate::user::user::{register_user, is_registration_enabled}; // log_user_in
use crate::auth::forms::{show_login_page, login_user};
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

    HttpServer::new(move || {
        App::new()
            // CORS are not needed at this stage
            // .wrap(Cors::permissive().allowed_origin_fn(|origin, _req_head| {
            //     return match origin.to_str() {
            //         Err(_) => false,
            //         Ok(val) => val.find("localhost").is_some()
            //     }
            // }))
            .app_data(pool.clone())
            .route("/login", web::post().to(auth::forms::login_user))
            .route("/register", web::post().to(auth::forms::process_registration))
            .route("/totp-setup", web::post().to(auth::forms::process_totp_setup))
    })
        .bind("127.0.0.1:8083")?
        .run()
        .await
}
