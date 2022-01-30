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
mod home;
mod auth;
mod errors;

use diesel::prelude::*;
use diesel::pg::PgConnection;
use std::env;

use actix_web::{get, post, web, http, App, HttpResponse, HttpServer, Responder};
use actix_cors::Cors;
use diesel::r2d2::{self, ConnectionManager};
use lettre::transport::smtp::authentication::Credentials;
use lettre::{Message, SmtpTransport, Transport};
use handlebars::Handlebars;
use crate::home::home::process_home;
use crate::user::user::{register_user, is_registration_enabled}; // log_user_in
use crate::auth::forms::{show_login_page, login_user};
use serde::Deserialize;
use crate::utilities::configuration::Configuration;

#[derive(Debug, Deserialize)]
struct Config {
    database: String,
}

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}

#[post("/send-email")]
async fn send_email(req_body: String) -> impl Responder {
    println!("Sending email");
    let email = Message::builder()
        .from("NoBody <nobody@domain.tld>".parse().unwrap())
        .reply_to("Yuin <yuin@domain.tld>".parse().unwrap())
        .to("Hei <hei@domain.tld>".parse().unwrap())
        .subject("Happy new year")
        .body(req_body)
        .unwrap();

    let creds = Credentials::new("smtp_username".to_string(), "smtp_password".to_string());

    // Open a remote connection to localhost
    let mailer = SmtpTransport::unencrypted_localhost();

    // Send the email
    return match mailer.send(&email) {
        Ok(_) => HttpResponse::Ok().body("Email sent"),
        Err(e) => HttpResponse::Ok().body(format!("Could not send email: {:?}", e)),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let mut handlebars = Handlebars::new();
    handlebars
        .register_templates_directory(".html", "./static/templates")
        .unwrap();
    let handlebars_ref = web::Data::new(handlebars);
    let config = Configuration::new();
    println!("{:?}", config.get_database());
    let manager = ConnectionManager::<PgConnection>::new(config.get_database());
    let pool = r2d2::Pool::builder()
        .build(manager)
        .expect("Failed to create pool.");

    HttpServer::new(move || {
        App::new()
            .wrap(Cors::permissive().allowed_origin_fn(|origin, _req_head| {
                return match origin.to_str() {
                    Err(_) => false,
                    Ok(val) => val.find("localhost").is_some()
                }
            }))
            .data(pool.clone())
            .app_data(handlebars_ref.clone())
            .route("/", web::get().to(home::home::process_home))
            .route("/login", web::get().to(auth::forms::show_login_page))
            .route("/login", web::post().to(auth::forms::login_user))
            .route("/registration", web::get().to(auth::forms::show_registration_page))
            .route("/register", web::post().to(auth::forms::process_registration))
            .route("/totp-setup", web::get().to(auth::forms::show_setup_totp_page))
            .route("/totp-setup", web::post().to(auth::forms::process_totp_setup))
    })
        .bind("127.0.0.1:8083")?
        .run()
        .await
}
